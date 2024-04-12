import datetime
import os

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import pyqtProperty
from jukebox_client.config import ASSETS, CONFIG
from jukebox_client.config.models import LanguageConfig

from enum import Enum
    
class Button(QtWidgets.QPushButton):
    def __init__(self, text: str):
        super().__init__(f"<{text}>")


class HeaderLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("HeaderLabel")


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, text: str):
        super().__init__(f"({text})")
        self.setObjectName("Title")


class TimeWidget(HeaderLabel):
    TIMER_INTERVAL = 1000
    TIME_FORMAT = ""

    def __init__(
        self,
        timer_interval: int = 60_000,
        time_format: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if time_format is None:
            time_format = "%H:%M"

        self.timer_interval = timer_interval
        self.time_format = time_format

        self.update_time()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.timer_interval)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    @QtCore.pyqtSlot()
    def update_time(self):
        time = datetime.datetime.now()
        self.setText(time.strftime(self.time_format))


class MusicEntry(QtWidgets.QWidget):
    def __init__(
        self, description: str, example: str | None = None, text: str | None = None
    ):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        self.descriptor = QtWidgets.QLabel()
        self.descriptor.setObjectName("MusicEntryDescriptor")
        layout.addWidget(self.descriptor)

        self.set_descriptor_text(description)

        self.entry = QtWidgets.QLineEdit()
        layout.addWidget(self.entry)

        if text is not None:
            self.entry.setText(text)

        if example is not None:
            self.entry.setPlaceholderText(example)

    def text(self) -> str | None:
        return self.entry.text() if self.entry.text() else None

    def setText(self, text: str):
        self.entry.setText(text)

    def set_descriptor_text(self, text: str):
        if not text.endswith(":"):
            text += ":"
        self.descriptor.setText(text)


class GradientButton(QtWidgets.QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setText("Click Me!")
        self.current_hue = 0

        self.setStyleSheet(self.generate_qss(self.current_hue))

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_style)
        self.timer.start(100)

    def generate_qss(self, hue: int) -> str:
        """Generate a QSS string to set the button color based on the hue."""
        color = QtGui.QColor.fromHsv(hue, 200, 200).name()
        return f"QPushButton {{ background-color: {color}; }}"

    def update_style(self) -> None:
        """Update the button's style by cycling through hues."""
        self.current_hue = (self.current_hue + 1) % 360
        self.setStyleSheet(self.generate_qss(self.current_hue))


class MusicWishWidget(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setObjectName("MusicWishWidget")

        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.music_title = MusicEntry("Musik Titel")
        layout.addWidget(self.music_title)

        self.artist = MusicEntry("Interpret")
        layout.addWidget(self.artist)

        self.sender_name = MusicEntry("Von")
        layout.addWidget(self.sender_name)

        self.receiver_name = MusicEntry("Für")
        layout.addWidget(self.receiver_name)

        self.message = MusicEntry("Nachricht")
        layout.addWidget(self.message)


class LanguageButton(QtWidgets.QPushButton):
    def __init__(self, language: LanguageConfig):
        super().__init__()
        self.setObjectName("LanguageButton")

        self._highlight = False
        self.language = language

        self.icon = QtGui.QIcon(language.language_icon)
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(48, 32))
        self.setToolTip(language.language_name.capitalize())

    @QtCore.pyqtProperty(bool)
    def highlight(self):
        return self._highlight

    @highlight.setter
    def highlight(self, state: bool):
        # Register change of state
        self._highlight = state
        # Update displayed style
        self.style().polish(self)


class LanguageSwitch(QtWidgets.QWidget):
    language_switched = QtCore.pyqtSignal(LanguageConfig)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.buttons = []

        self._language = CONFIG.languages[0]

        layout = QtWidgets.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        for index, language in enumerate(CONFIG.languages):
            language: LanguageConfig
            button = LanguageButton(language)
            if index == 0:
                button.highlight = True
            button.clicked.connect(self.on_language_change)
            layout.addWidget(button)
            self.buttons.append(button)

    @QtCore.pyqtSlot()
    def on_language_change(self):
        sender: LanguageButton = self.sender()
        if self._language == sender.language:
            return

        for button in self.buttons:
            button.highlight = button == sender

        self._language = sender.language
        self.language_switched.emit(self._language)

    def get_selected_language(self) -> LanguageConfig:
        return self._language
