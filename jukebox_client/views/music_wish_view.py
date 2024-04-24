from PyQt6 import QtWidgets, QtCore, QtGui
from jukebox_client.views.widgets import MusicWishWidget, Button, SubHeaderLabel
from .view import View
from jukebox_client.config import CONFIG


class MusicWishView(View):
    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.sub_heading = SubHeaderLabel(CONFIG.selected_language.heading_music_wish)
        layout.addWidget(self.sub_heading)

        self.music_wish_widget = MusicWishWidget()
        layout.addWidget(self.music_wish_widget)

        layout.addStretch()

        footer_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(footer_layout)

        self.quick_select_button = Button(CONFIG.selected_language.btn_quick_selection)
        footer_layout.addWidget(self.quick_select_button)

        self.send_button = Button(CONFIG.selected_language.btn_send)
        footer_layout.addWidget(self.send_button)
