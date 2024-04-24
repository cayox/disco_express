from jukebox_client.views import MainView, QuickSelectionDialog, InfoView
from PyQt6 import QtCore, QtWidgets
from jukebox_client.config import CONFIG, contains_slur
from jukebox_client.config.models import LanguageConfig
from jukebox_client.models import JukeBoxClient, MusicRequest, JukeBoxConnectionError
from jukebox_client.views.widgets import LoadingModal
import logging
from .controller import Controller
from jukebox_client.views import HomeView


class HomeController(Controller[HomeView]):
    def __init__(self):
        super().__init__(HomeView)

    def connect_view(self): ...

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()
        logging.info(f"Setting language: {language.language_name}")

        self.view.music_wish_button.setText(language.home_music_wish_btn)
        self.view.info_button.setText(language.home_info_btn)
        self.view.sub_heading.setText(language.heading_home)
        self.view.rotating_banner.setText(language.rotating_banner)
