import os.path

from PyQt6 import QtWidgets, QtCore, QtGui, QtSvg
from jukebox_client.config import CONFIG
from jukebox_client.config.models import LanguageConfig
from jukebox_client.views.widgets import Button


class ImageViewer(QtWidgets.QDialog):
    def __init__(self, image_path: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.path = image_path
        self.init_ui()

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time*1000)

    def init_ui(self):
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.setContentsMargins(48, 32, 48, 32)
        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        scroll_area.setWidget(w)

        main_lay.addWidget(scroll_area)

        layout = QtWidgets.QVBoxLayout(w)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setPixmap(QtGui.QPixmap(self.path))

        layout.addWidget(self.image_label)

        close_button = Button("Close")
        close_button.clicked.connect(self.close)
        main_lay.addWidget(close_button)

        scroll_area.setWidgetResizable(True)


class DocumentWidget(QtWidgets.QPushButton):
    ICON_SIZE = (36, 48)

    def __init__(self, path: str, name: str):
        super().__init__(" " * 2 + name)
        self.setObjectName("DocumentWidget")

        self.path = os.path.join(os.getcwd(), path)
        self.name = name

        self.setIcon(QtGui.QIcon(
        self.load_colored_svg(CONFIG.general.file_icon, CONFIG.colors.icon_color)))
        self.setIconSize(QtCore.QSize(*self.ICON_SIZE))

    def load_colored_svg(self, svg_path: str, color: str) -> QtGui.QPixmap:
        """Load and color an SVG, returning a QPixmap."""
        # Read SVG data
        with open(svg_path, "rb") as file:
            svg_data = file.read()

        # Replace color in SVG
        svg_data = svg_data.replace(b'fill="#000000"', f'fill="{color}"'.encode())

        # Render the modified SVG
        svg_renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data))
        image = QtGui.QPixmap(QtCore.QSize(*self.ICON_SIZE))  # Set the size as needed
        image.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(image)
        svg_renderer.render(painter)
        painter.end()

        return image


class DocumentDialog(QtWidgets.QDialog):
    MAX_COLS = 3

    def __init__(self, language: LanguageConfig):
        super().__init__()

        self.setObjectName("DocumentDialog")

        self.language = language

        self.setFixedWidth(1200)
        self.setMinimumHeight(800)

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time*1000)

        self._build_ui()

    def _build_ui(self):
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.setContentsMargins(48, 32, 48, 32)
        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        scroll_area.setWidget(w)

        main_lay.addWidget(scroll_area)

        layout = QtWidgets.QVBoxLayout(w)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        for index, document_path in enumerate(CONFIG.general.documents):
            doc_widget = DocumentWidget(document_path,
                                        name=self.language.document_names[index])
            doc_widget.clicked.connect(self._on_song_selected)

            layout.addWidget(doc_widget)

        close_button = Button("Close")
        close_button.clicked.connect(self.close)
        close_button.setMaximumHeight(1000)
        main_lay.addWidget(close_button)

        scroll_area.setWidgetResizable(True)

    @QtCore.pyqtSlot()
    def _on_song_selected(self):
        sender: DocumentWidget = self.sender()

        file = sender.path
        dialog = ImageViewer(file, parent=self)

        dialog.showMaximized()
        dialog.exec()
