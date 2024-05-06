import logging

from PyQt6 import QtCore

from disco_express.config import CONFIG
from disco_express.models.jukebox_client import JukeBoxClient, JukeBoxConnectionError
from disco_express.views import HomeView

from .controller import Controller


class HomeController(Controller[HomeView]):
    def __init__(self):
        super().__init__(HomeView)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.refresh_banner)
        self.timer.start()

        self.jukebox_client = JukeBoxClient(
            CONFIG.network.server_ip, CONFIG.network.server_port
        )
        self.refresh_banner()

    def connect_view(self): ...

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()

        self.view.music_wish_button.setText(language.home_music_wish_btn)
        self.view.info_button.setText(language.home_info_btn)
        self.view.sub_heading.setText(language.heading_home)
        self.view.rotating_banner.reset_text(language.rotating_banner)

    @QtCore.pyqtSlot()
    def refresh_banner(self):
        try:
            banner_texts = self.jukebox_client.get_banner_texts()
        except JukeBoxConnectionError as exc:
            logging.exception("Error retrieving banner texts", exc_info=exc)
            return

        for index, language in enumerate(CONFIG.languages):
            CONFIG.languages[index].rotating_banner = getattr(
                banner_texts, language.language_name
            )

        CONFIG.selected_language.rotating_banner = getattr(
            banner_texts, CONFIG.selected_language.language_name
        )
        self.set_selected_language()
