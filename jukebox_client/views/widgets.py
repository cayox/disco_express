import datetime

from PyQt6 import QtWidgets, QtCore, QtGui


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

        if not description.endswith(":"):
            description += ":"

        layout = QtWidgets.QVBoxLayout(self)
        self.descriptor = QtWidgets.QLabel(description)
        self.descriptor.setObjectName("MusicEntryDescriptor")
        layout.addWidget(self.descriptor)

        self.entry = QtWidgets.QLineEdit()
        layout.addWidget(self.entry)

        if text is not None:
            self.entry.setText(text)

        if example is not None:
            self.entry.setPlaceholderText(example)

    def text(self) -> str | None:
        return self.entry.text() if self.entry.text() else None


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

        self.interpret = MusicEntry("Interpret")
        layout.addWidget(self.interpret)

        self.sender_name = MusicEntry("Von")
        layout.addWidget(self.sender_name)

        self.receiver_name = MusicEntry("Für")
        layout.addWidget(self.receiver_name)

        self.message = MusicEntry("Nachricht")
        layout.addWidget(self.message)

class LanguageSwitch(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Language Switch")
        self.setGeometry(100, 100, 200, 60)
        self.setFixedSize(200, 60)
        self.is_english = True  # Start with English

        # Icons
        self.english_icon = QtGui.QIcon("icons/uk.png")
        self.german_icon = QtGui.QIcon("icons/germany.png")

        # English flag label
        self.label_english = QtWidgets.QLabel(self)
        self.label_english.setPixmap(self.english_icon.pixmap(QtCore.QSize(40, 25)))

        # German flag label
        self.label_german = QtWidgets.QLabel(self)
        self.label_german.setPixmap(self.german_icon.pixmap(QtCore.QSize(40, 25)))

        # Switch button
        self.switch_button = QtWidgets.QLabel(self)
        self.switch_button.setGeometry(70, 15, 60, 30)  # Position the switch in the middle

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.switch_button)

        # Background of the switch
        painter.setBrush(QtGui.QBrush(QtGui.QColor(200, 200, 200)))  # Grey background
        painter.drawRoundedRect(0, 0, 60, 30, 15, 15)

        # Moving circle of the switch
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FAFAFA")))
        if self.is_english:
            painter.drawEllipse(5, 5, 20, 20)
        else:
            painter.drawEllipse(35, 5, 20, 20)

    def mousePressEvent(self, event):
        self.is_english = not self.is_english
        self.update()
