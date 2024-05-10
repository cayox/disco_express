import os.path
import tempfile

from pdf2image import convert_from_path
from PIL import Image
from PyQt6 import QtCore, QtGui, QtWidgets

from disco_express.config import APP_CONFIG_ROOT, CONFIG
from disco_express.views.widgets import (
    Button,
    IconButton,
    SubHeaderLabel,
    build_accent1_glow_effect,
)

from .view import View


class ScrollableImage(QtWidgets.QLabel):
    """A label widget that displays an image with zoom in and zoom out capabilities."""
    def __init__(self, pixmap: QtGui.QPixmap):
        super().__init__()
        self.setObjectName("ImageViewer")
        self.pixmap = pixmap
        self.scale_factor = 2
        self.update_image()

    def update_image(self):
        """Update the image display based on the current scale factor."""
        scaled_pixmap = self.pixmap.scaled(
            self.size() * self.scale_factor,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled_pixmap)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def zoom_in(self):
        """Increase the scale factor for the image."""
        self.scale_factor = 1.25
        self.update_image()

    def zoom_out(self):
        """Decrease the scale factor for the image."""
        self.scale_factor = 0.75
        self.update_image()


class ImageViewer(QtWidgets.QDialog):
    """Dialog to display an image with zoom and scroll capabilities."""
    def __init__(self, image_path: str):
        super().__init__()
        self.setObjectName("ImageViewer")
        image = QtGui.QImage(image_path)
        self.image_label = ScrollableImage(QtGui.QPixmap.fromImage(image))
        self._init_ui()

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time * 1000)

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)
        layout.addWidget(scroll_area)

        self.close_button = Button("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        icon_size = 32

        self.zoom_in_button = IconButton(
            CONFIG.icons.zoom_in_icon,
            color=CONFIG.style.colors.accent1_glow,
            size=icon_size,
            parent=self,
        )
        self.zoom_in_button.clicked.connect(self.image_label.zoom_in)
        self.zoom_in_button.setFixedSize(icon_size, icon_size)

        self.zoom_out_button = IconButton(
            CONFIG.icons.zoom_out_icon,
            color=CONFIG.style.colors.accent1_glow,
            size=icon_size,
            parent=self,
        )
        self.zoom_out_button.clicked.connect(self.image_label.zoom_out)
        self.zoom_out_button.setFixedSize(icon_size, icon_size)

    def resizeEvent(self, a0: QtGui.QResizeEvent):  # noqa: N802
        """Handle the resize event."""
        self.resize(a0.size())
        super().resizeEvent(a0)

    def resize(self, a0: QtCore.QSize):
        """Adjust the dialog size based on the size of the viewport."""
        super().resize(a0)

        x_margin = int(a0.width() * 0.033)
        y_margin = int(a0.height() * 0.08)

        y_start = a0.height() - y_margin - self.close_button.height() - 32
        point = QtCore.QPoint(a0.width() - x_margin, y_start)
        self.zoom_in_button.move(point)

        self.zoom_out_button.move(
            QtCore.QPoint(a0.width() - x_margin, int(y_start + 40)),
        )


class PdfViewer(QtWidgets.QDialog):
    """Dialog to display a PDF file with zoom and scroll capabilities, using PyMuPDF for rendering.

    Loads all pages of the PDF into a single image for viewing.
    """
    def __init__(self, pdf_file: str):
        super().__init__()
        self.setObjectName("PdfViewer")
        self.pdf_file = pdf_file
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.image_label = ScrollableImage(self.load_pages())
        self.scroll_area.setWidget(self.image_label)

        self.close_button = Button("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        icon_size = 32

        self.zoom_in_button = IconButton(
            CONFIG.icons.zoom_in_icon,
            color=CONFIG.style.colors.accent1_glow,
            size=icon_size,
            parent=self,
        )
        self.zoom_in_button.clicked.connect(self.image_label.zoom_in)
        self.zoom_in_button.setFixedSize(icon_size, icon_size)

        self.zoom_out_button = IconButton(
            CONFIG.icons.zoom_out_icon,
            color=CONFIG.style.colors.accent1_glow,
            size=icon_size,
            parent=self,
        )
        self.zoom_out_button.clicked.connect(self.image_label.zoom_out)
        self.zoom_out_button.setFixedSize(icon_size, icon_size)

    def load_pages(self) -> QtGui.QPixmap:
        """Method to load all pages of a PDF and merge them to one image."""
        images = convert_from_path(self.pdf_file, dpi=200)
        if not images:
            return QtGui.QPixmap()

        # Combine images into a single image
        total_height = sum(image.height for image in images)
        max_width = max(image.width for image in images)
        combined_image = Image.new("RGB", (max_width, total_height))
        y_offset = 0

        for img in images:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.height

        with tempfile.NamedTemporaryFile() as file:
            # Save to a temporary file
            combined_image.save(file)
            return QtGui.QPixmap(file)

    def resizeEvent(self, a0: QtGui.QResizeEvent):  # noqa: N802
        """Handle the resize event."""
        self.resize(a0.size())
        super().resizeEvent(a0)

    def resize(self, a0: QtCore.QSize):
        """Adjust the dialog size based on the size of the viewport."""
        super().resize(a0)

        x_margin = int(a0.width() * 0.033)
        y_margin = int(a0.height() * 0.08)

        y_start = a0.height() - y_margin - self.close_button.height() - 32
        point = QtCore.QPoint(a0.width() - x_margin, y_start)
        self.zoom_in_button.move(point)

        self.zoom_out_button.move(
            QtCore.QPoint(a0.width() - x_margin, int(y_start + 40)),
        )


class DocumentWidget(QtWidgets.QPushButton):
    """Button to display a document."""
    ICON_SIZE = (36, 48)

    def __init__(self, path: str):
        name = os.path.basename(path).split(".")[0]
        super().__init__(name)
        self.setObjectName("DocumentWidget")

        self.setGraphicsEffect(build_accent1_glow_effect())

        self.path = path
        self.name = name


class InfoView(View):
    """View representing the Information page."""
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
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        scroll_area.setWidgetResizable(True)

        self.list_documents()

    @QtCore.pyqtSlot()
    def _on_doc_selected(self):
        sender: DocumentWidget = self.sender()

        file = sender.path
        dialog_class = PdfViewer if file.lower().endswith(".pdf") else ImageViewer
        dialog = dialog_class(file)

        dialog.showMaximized()
        dialog.exec()

    def list_documents(self):
        """List and display all available documents in the documents directory from the config.toml.

        Uses from config.toml:
        - CONFIG.general.documents_directory
        """
        while item := self.layout.takeAt(0):
            if widget := item.widget():
                widget.deleteLater()

        root = os.path.join(APP_CONFIG_ROOT, CONFIG.general.documents_directory)
        os.makedirs(root, exist_ok=True)

        for document in os.listdir(root):
            path = os.path.join(root, document)
            # ignore hidden files like .DS_Store
            if not os.path.isfile(path) or document.startswith("."):
                continue

            doc_widget = DocumentWidget(path)
            doc_widget.clicked.connect(self._on_doc_selected)

            self.layout.addWidget(doc_widget)
            self.documents.append(doc_widget)
