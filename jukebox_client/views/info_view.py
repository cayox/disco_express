import os.path

from PyQt6 import QtWidgets, QtCore, QtGui, QtSvg
from jukebox_client.config import CONFIG
from jukebox_client.config.models import LanguageConfig
from jukebox_client.views.widgets import Button, SubHeaderLabel
from .view import View
from .helpers import load_colored_svg


class ImageViewer(QtWidgets.QDialog):
    def __init__(self, image_path: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.setObjectName("ImageViewer")
        self.path = image_path
        self.init_ui()

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time * 1000)

    def init_ui(self):
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.setContentsMargins(48, 32, 48, 32)
        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        w.setObjectName("ImageViewer")
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


class DocumentWidget(Button):
    ICON_SIZE = (36, 48)

    def __init__(self, path: str):
        name = os.path.basename(path).split(".")[0]
        super().__init__(" " * 16 + name)
        self.setObjectName("DocumentWidget")

        self.setMinimumWidth(256)

        self.path = os.path.join(os.getcwd(), path)
        self.name = name

        self.setIcon(
            QtGui.QIcon(
                load_colored_svg(CONFIG.icons.file_icon, CONFIG.style.colors.text_color)
            )
        )
        self.setIconSize(QtCore.QSize(*self.ICON_SIZE))


class InfoView(View):
    MAX_COLS = 3

    def _build_ui(self):
        self.documents = []

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time * 1000)

        main_lay = QtWidgets.QVBoxLayout(self)

        self.sub_heading = SubHeaderLabel(CONFIG.selected_language.heading_information)
        main_lay.addWidget(self.sub_heading)

        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        w.setObjectName("InfoView")
        scroll_area.setWidget(w)

        main_lay.addWidget(scroll_area)

        self.layout = QtWidgets.QVBoxLayout(w)
        self.layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )

        scroll_area.setWidgetResizable(True)

        self.list_documents()

    @QtCore.pyqtSlot()
    def _on_song_selected(self):
        sender: DocumentWidget = self.sender()

        file = sender.path
        dialog = ImageViewer(file, parent=self)

        dialog.showMaximized()
        dialog.exec()

    def list_documents(self):
        while item := self.layout.takeAt(0):
            if widget := item.widget():
                widget.deleteLater()

        os.makedirs(CONFIG.general.documents_directory, exist_ok=True)
        for document in os.listdir(CONFIG.general.documents_directory):
            path = os.path.join(CONFIG.general.documents_directory, document)
            doc_widget = DocumentWidget(
                path
            )
            doc_widget.clicked.connect(self._on_song_selected)

            self.layout.addWidget(doc_widget)
            self.documents.append(doc_widget)
