import logging
import os
import sys

from PyQt6 import QtCore

from disco_express.config import APP_CONFIG_ROOT, CONFIG, contains_slur
from disco_express.config.models import Song
from disco_express.models import (
    ChartsManager,
    JukeBoxClient,
    JukeBoxConnectionError,
    MusicRequest,
)
from disco_express.models.jukebox_client import ServerStatus
from disco_express.views import MusicWishView, QuickSelectionDialog
from disco_express.views.widgets import LoadingModal

from .controller import Controller


class MusicController(Controller[MusicWishView]):
    """Controller controlling the behaviour of the MusicWishView."""
    music_request_sent = QtCore.pyqtSignal()

    def __init__(self):

        self._client = JukeBoxClient(
            CONFIG.network.server_ip,
            CONFIG.network.server_port,
        )

        super().__init__(MusicWishView)

        charts_path = os.path.join(APP_CONFIG_ROOT, CONFIG.general.charts_file)
        self.chart_manager = ChartsManager(charts_path)

    def connect_view(self):
        """Connect to MusicWishView and set langauges and check for connection."""
        logging.debug("Connecting controller to view")
        self.view.quick_select_button.clicked.connect(self.show_quick_selection)
        self.view.send_button.clicked.connect(self.send_music_request)

        self.set_selected_language()
        self.check_connection()

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        """Method to set the new language upon langauge change."""
        language = self.get_language()

        self.view.music_wish_widget.music_title.set_descriptor_text(
            language.music_title,
        )
        self.view.music_wish_widget.artist.set_descriptor_text(language.music_interpret)
        self.view.music_wish_widget.sender_name.set_descriptor_text(
            language.music_sender,
        )
        self.view.music_wish_widget.receiver_name.set_descriptor_text(
            language.music_receiver,
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
        """Method to display the QuickSelectionDialog and input the selected song, if available."""
        quick_selection_dialog = QuickSelectionDialog(self.get_language())
        if quick_selection_dialog.exec() <= 0:
            return

        song = quick_selection_dialog.selected_song
        self.view.music_wish_widget.music_title.setText(song.title)
        self.view.music_wish_widget.artist.setText(song.artist)

    @QtCore.pyqtSlot()
    def send_music_request(self):
        """Method to send the music request entered by the user.

        Checks if necessary inputs are available and checks for profanity before sending.
        Removes all input upon sending.
        """
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
        except JukeBoxConnectionError:
            logging.exception("Cannot send music request")
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
        """Method to retrieve the current server status and display it."""
        try:
            status = self._client.get_status()
            self.set_connection_status(status)
        except JukeBoxConnectionError:
            self.set_connection_status(ServerStatus.ERROR)

    def set_connection_status(self, status: ServerStatus):
        """Method to display the fetched status of the server.

        Closes the app with exit code 0 if the status is SHUTDOWN.
        """
        if status == ServerStatus.SHUTDOWN:
            sys.exit(0)

        enabled = status == ServerStatus.OK
        self.view.music_wish_widget.setEnabled(enabled)
        self.view.send_button.setEnabled(enabled)
        self.view.quick_select_button.setEnabled(enabled)

        self.view.music_wish_widget.status_widget.setVisible(not enabled)
        self.view.music_wish_widget.status_widget.setEnabled(True)
        self.view.music_wish_widget.status_widget.set_status(status)

    def check_profanity(self, music_request: MusicRequest) -> str | None:
        """Method to check for slurs in a music requests.

        Returns:
            the error text if a slur was found, else None
        """
        for text in music_request.dict().values():

            if text is None or not contains_slur(text):
                continue
            logging.info("Slur found in '%s'", text)
            return self.get_language().error_slur_found.format(text)
        return None
