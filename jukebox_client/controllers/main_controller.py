from jukebox_client.views import MainView, QuickSelectionDialog, DocumentDialog
from PyQt6 import QtCore, QtWidgets
from jukebox_client.config import CONFIG, contains_slur
from jukebox_client.config.models import LanguageConfig
from jukebox_client.models import JukeBoxClient, JukeBoxError, MusicRequest, JukeBoxConnectionError

class LanguageError(Exception):
    ...

class MainController(QtCore.QObject):
    def __init__(self, view: MainView):
        super().__init__()
        self._view = view

        self._client = JukeBoxClient(
            CONFIG.network.server_ip, CONFIG.network.server_port
        )

        self.connect_view()

    @property
    def view(self) -> MainView:
        return self._view

    def connect_view(self):
        self.view.info_button.clicked.connect(self.show_info)
        self.view.quick_select_button.clicked.connect(self.show_quick_selection)
        self.view.send_button.clicked.connect(self.send_music_request)
        self.view.language_widget.language_switched.connect(self.set_selected_language)

        self.set_selected_language()
        self.check_connection()

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()
        self.view.title.setText(f"({CONFIG.general.app_name})")

        self.view.music_wish_widget.music_title.set_descriptor_text(language.music_title)
        self.view.music_wish_widget.artist.set_descriptor_text(language.music_interpret)
        self.view.music_wish_widget.sender_name.set_descriptor_text(language.music_sender)
        self.view.music_wish_widget.receiver_name.set_descriptor_text(language.music_receiver)
        self.view.music_wish_widget.message.set_descriptor_text(language.music_message)

        self.view.send_button.setText(f"<{language.btn_send}>")
        self.view.info_button.setText(f"<{language.btn_info}>")
        self.view.quick_select_button.setText(f"<{language.btn_quick_selection}>")

        self.view.connection_lost_label.setText(language.error_no_connection_to_server)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(CONFIG.general.server_refresh_interval*1000)
        self.timer.timeout.connect(self.check_connection)
        self.timer.start()

    def show_error(self, text: str):
        QtWidgets.QMessageBox.critical(self.view, "Error", text)

    def check_profanity(self, music_request: MusicRequest) -> str | None:
        for key, text in music_request.dict().items():

            if text is None or not contains_slur(text):
                continue
            return self.get_language().error_slur_found.format(text)

    def get_language(self) -> LanguageConfig:
        return self.view.language_widget.get_selected_language()

    @QtCore.pyqtSlot()
    def show_info(self):
        quick_selection_dialog = DocumentDialog(self.get_language())
        quick_selection_dialog.exec()

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

    @QtCore.pyqtSlot()
    def check_connection(self):
        try:
            self._client.heartbeat()
            self.set_connection_status(True)
        except Exception:
            self.set_connection_status(False)

    def set_connection_status(self, enabled: bool):
        self.view.music_wish_widget.setEnabled(enabled)
        # self.view.title.setEnabled(enabled)
        # self.view.time_widget.setEnabled(enabled)
        # self.view.date_widget.setEnabled(enabled)
        self.view.send_button.setEnabled(enabled)
        self.view.quick_select_button.setEnabled(enabled)

        self.view.connection_lost_label.setVisible(not enabled)

