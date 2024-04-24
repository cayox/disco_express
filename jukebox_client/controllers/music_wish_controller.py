from jukebox_client.views import MainView, QuickSelectionDialog, InfoView
from PyQt6 import QtCore, QtWidgets
from jukebox_client.config import CONFIG, contains_slur
from jukebox_client.config.models import Song
from jukebox_client.models import (
    JukeBoxClient,
    MusicRequest,
    JukeBoxConnectionError,
    ChartsManager,
)
from jukebox_client.models.jukebox_client import ServerStatus
from jukebox_client.views.widgets import LoadingModal
import logging
from .controller import Controller
from jukebox_client.views import MusicWishView


class MusicController(Controller[MusicWishView]):
    music_request_sent = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__(MusicWishView)

        self._client = JukeBoxClient(
            CONFIG.network.server_ip, CONFIG.network.server_port
        )

        self.chart_manager = ChartsManager(CONFIG.general.charts_file)

    def connect_view(self):
        logging.debug("Connecting controller to view")
        self.view.quick_select_button.clicked.connect(self.show_quick_selection)
        self.view.send_button.clicked.connect(self.send_music_request)

        self.set_selected_language()
        self.check_connection()

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()
        logging.info(f"Setting language: {language.language_name}")

        self.view.music_wish_widget.music_title.set_descriptor_text(
            language.music_title
        )
        self.view.music_wish_widget.artist.set_descriptor_text(language.music_interpret)
        self.view.music_wish_widget.sender_name.set_descriptor_text(
            language.music_sender
        )
        self.view.music_wish_widget.receiver_name.set_descriptor_text(
            language.music_receiver
        )
        self.view.music_wish_widget.message.set_descriptor_text(language.music_message)

        self.view.send_button.setText(language.btn_send)
        self.view.quick_select_button.setText(language.btn_quick_selection)


        self.view.sub_heading.setText(language.heading_music_wish)

        self.check_connection()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(CONFIG.general.server_refresh_interval * 1000)
        self.timer.timeout.connect(self.check_connection)
        self.timer.start()

    @QtCore.pyqtSlot()
    def show_quick_selection(self):
        quick_selection_dialog = QuickSelectionDialog(self.get_language())
        if quick_selection_dialog.exec() <= 0:
            return

        song = quick_selection_dialog.selected_song
        self.view.music_wish_widget.music_title.setText(song.title)
        self.view.music_wish_widget.artist.setText(song.artist)

    @QtCore.pyqtSlot()
    def send_music_request(self):
        title = self.view.music_wish_widget.music_title.text()
        if title is None:
            self.show_error(self.get_language().error_no_title)
            return

        interpret = self.view.music_wish_widget.artist.text()
        if interpret is None:
            self.show_error(self.get_language().error_no_interpret)
            return

        music_request = MusicRequest(
            title=title,
            interpret=interpret,
            sender=self.view.music_wish_widget.sender_name.text(),
            receiver=self.view.music_wish_widget.receiver_name.text(),
            message=self.view.music_wish_widget.message.text(),
        )
        error_message = self.check_profanity(music_request)
        if error_message is not None:
            self.show_error(error_message)
            return

        try:
            error = self._client.send_music_request(music_request)
        except JukeBoxConnectionError as e:
            if CONFIG.general.debug:
                raise e
            self.show_error("Cannot reach the Jukebox Server. Please inform an Admin!")
            return

        if error is not None:
            if error.status == "unavailable":
                self.show_error(self.get_language().error_dj_unavailable)
            else:
                self.show_error(self.get_language().error_network)

        self.chart_manager.add_song(song=Song(title=title, artist=interpret))

        loading_modal = LoadingModal()
        loading_modal.exec()

        self.view.music_wish_widget.music_title.setText("")
        self.view.music_wish_widget.artist.setText("")
        self.view.music_wish_widget.sender_name.setText("")
        self.view.music_wish_widget.receiver_name.setText("")
        self.view.music_wish_widget.message.setText("")

        self.music_request_sent.emit()

    @QtCore.pyqtSlot()
    def check_connection(self):
        try:
            status = self._client.get_status()
            self.set_connection_status(status)
        except Exception:
            self.set_connection_status(ServerStatus.ERROR)

    def set_connection_status(self, status: ServerStatus):
        enabled = status == ServerStatus.OK
        self.view.music_wish_widget.setEnabled(enabled)
        self.view.send_button.setEnabled(enabled)
        self.view.quick_select_button.setEnabled(enabled)

        self.view.music_wish_widget.status_widget.setVisible(not enabled)
        self.view.music_wish_widget.status_widget.setEnabled(True)
        self.view.music_wish_widget.status_widget.set_status(status)

    def check_profanity(self, music_request: MusicRequest) -> str | None:
        for key, text in music_request.dict().items():

            if text is None or not contains_slur(text):
                continue
            logging.info(f"Slur found in '{text}'")
            return self.get_language().error_slur_found.format(text)
