from PyQt6 import QtCore, QtWidgets

from disco_express.config import CONFIG
from disco_express.views.widgets import (
    Button,
    StatusWidget,
    SubHeaderLabel,
    build_accent1_glow_effect,
)

from .view import View


class MusicEntryDescriptor(QtWidgets.QLabel):
    def setText(self, a0: str):  # noqa: N802
        super().setText(f"|{a0}¬")
        self.setObjectName("MusicEntryDescriptor")
        self.setMinimumWidth(196)
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )


class MusicEntry(QtWidgets.QWidget):
    def __init__(
        self,
        description: str,
        example: str | None = None,
        text: str | None = None,
        max_length: int = 32,
    ):
        super().__init__()

        layout = QtWidgets.QHBoxLayout(self)
        self.descriptor = MusicEntryDescriptor()
        layout.addWidget(self.descriptor)

        self.set_descriptor_text(description)

        self.entry = QtWidgets.QLineEdit()
        self.entry.setMaxLength(max_length)
        layout.addWidget(self.entry)

        if text is not None:
            self.entry.setText(text)

        if example is not None:
            self.entry.setPlaceholderText(example)

    def text(self) -> str | None:
        return self.entry.text() if self.entry.text() else None

    def setText(self, text: str):  # noqa: N802
        self.entry.setText(text)

    def set_descriptor_text(self, text: str):
        self.descriptor.setText(text)


class MusicWishWidget(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setObjectName("MusicWishWidget")

        self.setGraphicsEffect(build_accent1_glow_effect())

        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.status_widget = StatusWidget(
            visible=False,
        )
        layout.addWidget(self.status_widget)

        self.music_title = MusicEntry(
            CONFIG.selected_language.music_title,
            max_length=CONFIG.general.max_input_length,
        )
        layout.addWidget(self.music_title)

        self.artist = MusicEntry(
            CONFIG.selected_language.music_interpret,
            max_length=CONFIG.general.max_input_length,
        )
        layout.addWidget(self.artist)

        self.sender_name = MusicEntry(
            CONFIG.selected_language.music_sender,
            max_length=CONFIG.general.max_input_length,
        )
        layout.addWidget(self.sender_name)

        self.receiver_name = MusicEntry(
            CONFIG.selected_language.music_receiver,
            max_length=CONFIG.general.max_input_length,
        )
        layout.addWidget(self.receiver_name)

        self.message = MusicEntry(
            CONFIG.selected_language.music_message,
            max_length=CONFIG.general.max_input_length_message,
        )
        layout.addWidget(self.message)


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
