from jukebox_client.views import MainView
from PyQt6 import QtCore, QtWidgets
from jukebox_client.config import CONFIG, is_slur
from jukebox_client.config.models import Language
from jukebox_client.models import JukeBoxClient, JukeBoxError, MusicRequest


class MainController(QtCore.QObject):
    def __init__(self, view: MainView):
        super().__init__()
        self._view = view

        self._client = JukeBoxClient(CONFIG.network.server_ip,
                                     CONFIG.network.server_port)

        self.english = False

        self.connect_view()

    @property
    def view(self) -> MainView:
        return self._view

    def connect_view(self):
        self.view.info_button.clicked.connect(self.show_info)
        self.view.quick_select_button.clicked.connect(self.show_quick_selection)
        self.view.send_button.clicked.connect(self.send_music_request)

    def show_error(self, text: str):
        QtWidgets.QMessageBox.critical(self.view, "Error", text)

    def check_profanity(self, music_request: MusicRequest) -> str | None:
        for key, text in music_request.dict().items():
            if not is_slur(text):
                continue
            return self.get_language().slur_found_error.format(text)

    def get_language(self) -> Language:
        if self.english:
            return CONFIG.languages.english
        return CONFIG.languages.german

    @QtCore.pyqtSlot()
    def show_info(self):
        raise NotImplementedError

    @QtCore.pyqtSlot()
    def show_quick_selection(self):
        raise NotImplementedError

    @QtCore.pyqtSlot()
    def send_music_request(self):
        title = self.view.music_wish_widget.music_title.text()
        if title is None:
            self.show_error(self.get_language().error_no_title)
            return

        interpret = self.view.music_wish_widget.interpret.text()
        if interpret is None:
            self.show_error(self.get_language().error_no_interpret)
            return

        music_request = MusicRequest(
            title=title,
            interpret=interpret,
            sender=self.view.music_wish_widget.sender_name.text(),
            receiver=self.view.music_wish_widget.receiver_name.text(),
            message=self.view.music_wish_widget.message.text()
        )
        error_message = self.check_profanity(music_request)
        if error_message is not None:
            self.show_error(error_message)
            return

        error = self._client.send_music_request(music_request)
        if error is not None:
            if error.status == "unavailable":
                self.show_error(self.get_language().error_dj_unavailable)
            else:
                self.show_error(self.get_language().error_network)
