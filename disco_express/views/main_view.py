import os

from PyQt6 import QtCore, QtGui, QtWidgets

from disco_express.config import APP_CONFIG_ROOT, CONFIG
from disco_express.views.widgets import IconButton, TimeWidget, TitleLabel

from .view import View


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainView")
        self.background = QtGui.QPixmap(
            os.path.join(APP_CONFIG_ROOT, CONFIG.style.background_image),
        )
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def paintEvent(self, event: QtGui.QPaintEvent):  # noqa: N802, ARG002, inherited
        painter = QtGui.QPainter(self)
        painter.setOpacity(1 - CONFIG.style.background_darkness_factor)
        painter.drawPixmap(self.rect(), self.background)


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainView")

        self._build_ui()

        # path = os.path.join(APP_CONFIG_ROOT, CONFIG.general.screen_saver_images)
        # self.screen_saver = ScreenSaver(path)
        #
        # self.screen_saver_timer = QtCore.QTimer(self)
        # self.screen_saver_timer.setSingleShot(True)
        # self.screen_saver_timer.timeout.connect(self.show_screen_saver)
        # self.screen_saver_timer.start(CONFIG.general.screen_saver_start_time*1000)
        #
        # self.last_mouse_position = QtGui.QCursor.pos()

    def _build_ui(self):
        self.widget = CentralWidget()
        self.setCentralWidget(self.widget)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.widget.setLayout(layout)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(32, 12, 32, 12)
        layout.addLayout(header_layout)

        self.home_button = IconButton(
            CONFIG.icons.home_icon,
            CONFIG.style.colors.accent1_glow,
            128,
        )
        header_layout.addWidget(self.home_button)

        self.time_widget = TimeWidget()
        header_layout.addWidget(self.time_widget)

        header_layout.addStretch()

        self.title = TitleLabel("Disco Express")
        header_layout.addWidget(self.title)

        header_layout.addStretch()

        self.date_widget = TimeWidget(time_format="%d.%m.%y")
        header_layout.addWidget(self.date_widget)

        self.stack = QtWidgets.QStackedWidget()
        layout.addWidget(self.stack)

    def add_page(self, page: View) -> int:
        self.stack.addWidget(page)
        return self.stack.count() - 1

    def closeEvent(self, event: QtGui.QCloseEvent):  # noqa: N802, inherited
        """Override the close event to prevent closing."""
        event.ignore()  # Ignore the close event

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):  # noqa: N802, ARG002, inherited
        """Dismiss the screensaver if the mouse is moved."""
        current_position = QtGui.QCursor.pos()
        if current_position != self.last_mouse_position:
            self.hide()
            self.screen_saver_timer.start(CONFIG.general.screen_saver_start_time * 1000)

    def show_screen_saver(self):
        self.screen_saver.showFullScreen()
