import logging
from typing import Generic, TypeVar

from PyQt6 import QtCore, QtWidgets

from disco_express.config import CONFIG
from disco_express.config.models import LanguageConfig

V = TypeVar("V")


class Controller(QtCore.QObject, Generic[V]):
    def __init__(self, view_class: type[V]):
        super().__init__()

        self._view = view_class()

        self.connect_view()

    @property
    def view(self) -> V:
        return self._view

    def show_error(self, text: str):
        logging.error("Displaying error: %s", text)
        QtWidgets.QMessageBox.critical(self.view, "Error", text)

    def get_language(self) -> LanguageConfig:
        return CONFIG.selected_language

    def connect_view(self):
        raise NotImplementedError

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        raise NotImplementedError
