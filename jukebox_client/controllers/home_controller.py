from PyQt6 import QtCore

from jukebox_client.views import HomeView

from .controller import Controller


class HomeController(Controller[HomeView]):
    def __init__(self):
        super().__init__(HomeView)

    def connect_view(self): ...

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()

        self.view.music_wish_button.setText(language.home_music_wish_btn)
        self.view.info_button.setText(language.home_info_btn)
        self.view.sub_heading.setText(language.heading_home)
        self.view.rotating_banner.setText(language.rotating_banner)
