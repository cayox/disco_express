from PyQt6 import QtCore, QtWidgets
import logging
from jukebox_client.config.models import LanguageConfig
from typing import Type, TypeVar, Generic
from jukebox_client.config import CONFIG


V = TypeVar("V")


class Controller(QtCore.QObject, Generic[V]):
    def __init__(self, view_class: Type[V]):
        super().__init__()

        self._view = view_class()

        self.connect_view()

    @property
    def view(self) -> V:
        return self._view

    def show_error(self, text: str):
        logging.error(f"Displaying error: {text}")
        QtWidgets.QMessageBox.critical(self.view, "Error", text)

    def get_language(self) -> LanguageConfig:
        return CONFIG.selected_language

    def connect_view(self):
        raise NotImplementedError

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        raise NotImplementedError
