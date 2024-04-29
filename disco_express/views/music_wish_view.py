from PyQt6 import QtWidgets

from disco_express.config import CONFIG
from disco_express.views.widgets import Button, MusicWishWidget, SubHeaderLabel

from .view import View


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
