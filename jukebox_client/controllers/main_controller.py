import logging

from PyQt6 import QtCore

from jukebox_client.config import CONFIG
from jukebox_client.views import MainView

from .controller import Controller
from .home_controller import HomeController
from .info_controller import InfoController
from .music_wish_controller import MusicController


class MainController(Controller[MainView]):
    def __init__(self):
        super().__init__(MainView)

    @property
    def view(self) -> MainView:
        return self._view

    def connect_view(self):
        self.ctrl_home = HomeController()
        self.home_index = self.view.add_page(self.ctrl_home.view)
        self.view.home_button.clicked.connect(lambda: self.switch_page(self.home_index))
        self.ctrl_home.view.language_widget.language_switched.connect(
            self.set_selected_language,
        )

        self.ctrl_music = MusicController()
        self.ctrl_music.music_request_sent.connect(
            lambda: self.switch_page(self.home_index),
        )
        self.music_index = self.view.add_page(self.ctrl_music.view)
        self.ctrl_home.view.music_wish_button.clicked.connect(
            lambda: self.switch_page(self.music_index),
        )

        self.ctrl_info = InfoController()
        self.view.add_page(self.ctrl_info.view)
        self.info_index = self.view.add_page(self.ctrl_info.view)
        self.ctrl_home.view.info_button.clicked.connect(
            lambda: self.switch_page(self.info_index),
        )

        self.set_selected_language()
        self.switch_page(0)

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.ctrl_home.view.language_widget.get_selected_language()
        logging.info("Setting language: %s", language.language_name)
        self.view.title.setText(f"({CONFIG.general.app_name})")

        CONFIG.selected_language = language
        self.ctrl_music.set_selected_language()
        self.ctrl_info.set_selected_language()
        self.ctrl_home.set_selected_language()

    def switch_page(self, index: int):
        self.view.home_button.setVisible(index != self.home_index)
        self.view.stack.setCurrentIndex(index)
