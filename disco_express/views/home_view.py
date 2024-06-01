from typing import Any

from PyQt6 import QtCore, QtWidgets

from disco_express.config import CONFIG
from disco_express.views.widgets import (
    Button,
    LanguageSwitch,
    RotatingBanner,
    SubHeaderLabel,
)

from .view import View


class NavigationButton(Button):
    """Button with custom style via QSS Stylesheet."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.setObjectName("NavigationButton")


class HomeView(View):
    """View representing the home page."""

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        self.sub_heading = SubHeaderLabel(CONFIG.selected_language.heading_home)
        layout.addWidget(self.sub_heading)

        button_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(128)

        self.music_wish_button = NavigationButton(
            CONFIG.selected_language.home_music_wish_btn,
        )

        button_layout.addWidget(self.music_wish_button)

        self.info_button = NavigationButton(CONFIG.selected_language.home_info_btn)
        button_layout.addWidget(self.info_button)

        self.language_widget = LanguageSwitch()
        layout.addWidget(self.language_widget)

        layout.addStretch()

        self.rotating_banner = RotatingBanner(CONFIG.selected_language.rotating_banner)
        self.rotating_banner.setFixedWidth(1600)
        layout.addWidget(self.rotating_banner)
