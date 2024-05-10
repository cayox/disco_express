# ruff: noqa: D102
import datetime
import os
from typing import Any

from PyQt6 import QtCore, QtGui, QtWidgets

from disco_express.config import APP_CONFIG_ROOT, CONFIG
from disco_express.config.models import LanguageConfig
from disco_express.models.jukebox_client import ServerStatus

from .helpers import load_colored_svg


def build_accent1_glow_effect() -> QtWidgets.QGraphicsDropShadowEffect:
    """Function to build a glow effect from CONFIG.style.colors.accent1_glow."""
    effect = QtWidgets.QGraphicsDropShadowEffect()
    effect.setOffset(0)
    effect.setBlurRadius(CONFIG.style.ui_glow_strength)
    effect.setColor(QtGui.QColor(CONFIG.style.colors.accent1_glow))
    return effect


def build_highlight_glow_effect() -> QtWidgets.QGraphicsDropShadowEffect:
    """Function to build a glow effect from CONFIG.style.colors.highlight_glow."""
    effect = QtWidgets.QGraphicsDropShadowEffect()
    effect.setOffset(0)
    effect.setBlurRadius(CONFIG.style.text_glow_strength)
    effect.setColor(QtGui.QColor(CONFIG.style.colors.highlight_glow))
    return effect


class GlowLabel(QtWidgets.QLabel):
    """Label where a glow effect is applied."""
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.setGraphicsEffect(build_highlight_glow_effect())


class SubHeaderLabel(GlowLabel):
    """Label that is styled as a sub header in QSS stylesheet.

    Has glow effect.
    """
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("SubHeaderLabel")
        self.setWordWrap(True)


class IconButton(QtWidgets.QPushButton):
    """Button which displays an icon.

    Has glow effect.

    Args:
        icon: the icon path to display.
        color: the wanted color, works only for SVGs.
        size: the wanted size for the icon.
    """
    def __init__(self, icon: str, color: str, size: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("IconButton")

        self.setIcon(QtGui.QIcon(load_colored_svg(icon, color, size)))

        self.setGraphicsEffect(build_accent1_glow_effect())


class Button(QtWidgets.QPushButton):
    """Button which formats the text in the respective JukeBox font.

    Has glow effect.
    """
    def __init__(self, text: str):
        super().__init__()
        self.setText(text)

        self.setGraphicsEffect(build_accent1_glow_effect())

    def setText(self, text: str):  # noqa: N802
        super().setText(f"<{text}>")


class HeaderLabel(GlowLabel):
    """Label that is styled as a header in QSS stylesheet.

    Has glow effect.
    """
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.setObjectName("HeaderLabel")


class TitleLabel(GlowLabel):
    """Label that is styled as a title in QSS stylesheet.

    Has glow effect.
    """
    def __init__(self, text: str):
        super().__init__(f"({text})")
        self.setObjectName("Title")


class TimeWidget(HeaderLabel):
    """Widget representing a time or date, which updates automatically.

    Args:
        timer_interval: the intervall the time should be updated.
        time_format: the format in which the time should be represented.
            See datetime library for format options. Defaults to "%H:%M".
    """

    def __init__(
        self,
        timer_interval: int = 60_000,
        time_format: str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)

        if time_format is None:
            time_format = "%H:%M"

        self.setObjectName("TimeWidget")

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


class LanguageButton(QtWidgets.QPushButton):
    """Button representing a Language.

    Displays the icon of the language.

    Args:
        language: the language to represent.
    """
    def __init__(self, language: LanguageConfig):
        super().__init__()
        self.setObjectName("LanguageButton")

        self._highlight = False
        self.language = language

        icon_path = os.path.join(APP_CONFIG_ROOT, language.language_icon)
        self.icon = QtGui.QIcon(icon_path)
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(48, 32))
        self.setToolTip(language.language_name.capitalize())

    @QtCore.pyqtProperty(bool)
    def highlight(self) -> bool:
        """Getter for highlighting the button via QSS stylesheet."""
        return self._highlight

    @highlight.setter
    def highlight(self, state: bool):
        """Setter for highlighting the button via QSS stylesheet."""
        # Register change of state
        self._highlight = state
        # Update displayed style
        self.style().polish(self)


class LanguageSwitch(QtWidgets.QWidget):
    """Widget for switching languages.

    Uses all languages configured in the config.toml:
    - CONFIG.languages
    """
    language_switched = QtCore.pyqtSignal(LanguageConfig)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
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
        """Callback for handling when the language was changed."""
        sender: LanguageButton = self.sender()
        if self._language == sender.language:
            return

        for button in self.buttons:
            button.highlight = button == sender

        self._language = sender.language
        self.language_switched.emit(self._language)

    def get_selected_language(self) -> LanguageConfig:
        """Retrieve the selected language."""
        return self._language


class StatusWidget(QtWidgets.QWidget):
    """Widget displaying the current server status, used for errors.

    Sets text based on teh config.toml:
    - CONFIG.selected_language.error_dj_unavailable
    - CONFIG.selected_language.error_no_connection_to_server

    Args:
        visible: whether the widget should be visible upon startup
    """
    ICON_SIZE = 48

    def __init__(self, visible: bool = False):
        super().__init__()
        self.setObjectName("StatusWidget")

        text = CONFIG.selected_language.error_no_connection_to_server

        self.setVisible(visible)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.icon_label1 = QtWidgets.QLabel()
        self.icon_label1.setObjectName("StatusWidget")
        layout.addWidget(self.icon_label1)

        self.label = GlowLabel(text)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("StatusWidget")
        layout.addWidget(self.label)

        self.icon_label2 = QtWidgets.QLabel()
        self.icon_label2.setObjectName("StatusWidget")
        layout.addWidget(self.icon_label2)

        layout.addStretch()

    def setText(self, text: str):  # noqa: N802, inherited
        self.label.setText(text)

    def set_status(self, status: ServerStatus):
        """Method to set the text and icons of the StatusWidget.

        Sets text based on teh config.toml:
        - CONFIG.selected_language.error_dj_unavailable
        - CONFIG.selected_language.error_no_connection_to_server
        """
        if status == ServerStatus.UNAVAILABLE:
            color = CONFIG.style.colors.red
            icon = load_colored_svg(
                CONFIG.icons.unavailable_icon,
                color,
            )
            text = CONFIG.selected_language.error_dj_unavailable
        elif status == ServerStatus.ERROR:
            color = CONFIG.style.colors.red
            icon = load_colored_svg(
                CONFIG.icons.error_icon,
                color,
            )
            text = CONFIG.selected_language.error_no_connection_to_server
        else:
            return

        self.icon_label1.setPixmap(icon)
        self.icon_label2.setPixmap(icon)
        self.label.setText(text)
        self.label.setStyleSheet(
            f"""
            QLabel {{
                color: {color};
                font-size: 24px;
            }}""",
        )


class LoadingModal(QtWidgets.QDialog):
    """Modal showing a loading process.

    Automatically increases the progressbar and displays the text configured in the config.toml:
    - CONFIG.general.wish_sending_time
    - CONFIG.selected_language.loading_description
    - CONFIG.selected_language.loading_success
    """
    def __init__(self):
        super().__init__()

        self.setObjectName("LoadingModal")

        self._loading_text_index = 0

        self._build_ui()

        interval = CONFIG.general.wish_sending_time // len(
            CONFIG.selected_language.loading_description,
        )
        self.label_timer = QtCore.QTimer()
        self.label_timer.setInterval(interval * 1000)
        self.label_timer.timeout.connect(self._on_label_timer_timeout)
        self.label_timer.start()

        self.progress_timer = QtCore.QTimer()
        self.progress_timer.setInterval(CONFIG.general.wish_sending_time * 10)
        self.progress_timer.timeout.connect(self._on_progress_timer_timeout)
        self.progress_timer.start()

        self.close_timer = QtCore.QTimer()
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(lambda: self.accept())
        self.close_timer.setInterval(3000)

    def _build_ui(self):
        self.setMinimumWidth(400)
        layout = QtWidgets.QVBoxLayout(self)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimumHeight(32)
        self.progress_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setGraphicsEffect(build_highlight_glow_effect())

        layout.addWidget(self.progress_bar)

        self.loading_label = GlowLabel(
            CONFIG.selected_language.loading_description[self._loading_text_index],
        )
        self._loading_text_index += 1
        self.loading_label.setObjectName("LoadingLabel")
        layout.addWidget(self.loading_label)

        self.success_label = GlowLabel(CONFIG.selected_language.loading_success)
        self.success_label.setObjectName("LoadingSuccessLabel")
        self.success_label.setVisible(False)
        layout.addWidget(self.success_label)

    @QtCore.pyqtSlot()
    def _on_label_timer_timeout(self):
        self.loading_label.setText(
            CONFIG.selected_language.loading_description[self._loading_text_index],
        )
        if (
            self._loading_text_index
            < len(CONFIG.selected_language.loading_description) - 1
        ):
            self._loading_text_index += 1

    @QtCore.pyqtSlot()
    def _on_progress_timer_timeout(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        if not self.progress_bar.value() >= self.progress_bar.maximum():
            return

        self.progress_bar.setVisible(False)
        self.loading_label.setVisible(False)
        self.success_label.setVisible(True)
        self.close_timer.start()
        self.progress_timer.stop()


class RotatingBanner(GlowLabel):
    """Banner which scrolls through the text automatically.

    Args:
        text: the text to rotate
    """
    def __init__(self, text: str):
        super().__init__()
        self.setObjectName("RotatingLabel")

        self.reset_text(text)

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.rotate_text)
        self.timer.start(CONFIG.general.banner_speed)

    @QtCore.pyqtSlot()
    def rotate_text(self):
        """Method to rotate the text by appending the first letter to the end."""
        current_text = self.text()
        rotated_text = current_text[1:] + current_text[0]
        self.setText(rotated_text)

    def reset_text(self, text: str):
        """Method to reset/set new `text`."""
        min_text_length = 100
        while len(text) < min_text_length:
            text = text * 2
        self.setText(text)
