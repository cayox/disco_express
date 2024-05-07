import glob
import os

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor


class ScreenSaver(QtWidgets.QWidget):
    def __init__(self, image_folder: str):
        super().__init__()
        self.init_ui()
        self.load_images(image_folder)

    def init_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.showMaximized()
        self.setCursor(Qt.CursorShape.BlankCursor)
        self.last_mouse_position = QCursor.pos()

    def load_images(self, folder: str):
        """Load all images from the specified folder."""
        self.images = glob.glob(os.path.join(folder, "*.jpg")) + glob.glob(
            os.path.join(folder, "*.png")
        )
        self.image_index = 0

        if not self.images:
            QtWidgets.QMessageBox.warning(
                self, "Warning", f"No Screen Saver Images found in {folder}"
            )
            return

        self.update_image()

    def update_image(self):
        """Update the label with the next image."""
        pixmap = QtGui.QPixmap(self.images[self.image_index])
        self.label.setPixmap(
            pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.image_index = (self.image_index + 1) % len(self.images)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):  # noqa: N802, ARG002, inherited
        """Dismiss the screensaver if the mouse is moved."""
        current_position = QtGui.QCursor.pos()
        if current_position != self.last_mouse_position:
            self.hide()
