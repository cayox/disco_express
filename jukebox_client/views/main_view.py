from PyQt6 import QtWidgets, QtCore, QtGui
from jukebox_client.views.widgets import TitleLabel, TimeWidget, MusicWishWidget, LanguageSwitch


class MainView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainView")

        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.setLayout(layout)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(256)
        layout.addLayout(header_layout)

        self.time_widget = TimeWidget()
        header_layout.addWidget(self.time_widget)
        header_layout.addStretch()

        self.title = TitleLabel("Disco Express")
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.date_widget = TimeWidget(time_format="%d.%m.%y")
        header_layout.addWidget(self.date_widget)

        layout.addStretch()

        self.music_wish_widget = MusicWishWidget()
        layout.addWidget(self.music_wish_widget)

        self.language = LanguageSwitch()
        layout.addWidget(self.language)

        layout.addStretch()

        footer_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(footer_layout)

        self.quick_select_button = QtWidgets.QPushButton("<Schnell Auswahl>")
        footer_layout.addWidget(self.quick_select_button)

        self.info_button = QtWidgets.QPushButton("<Information>")
        footer_layout.addWidget(self.info_button)

        self.send_button = QtWidgets.QPushButton("<Abschicken>")
        footer_layout.addWidget(self.send_button)
