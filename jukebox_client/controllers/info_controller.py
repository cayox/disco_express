import os

from jukebox_client.views import MainView, QuickSelectionDialog, InfoView
from PyQt6 import QtCore, QtWidgets
from jukebox_client.config import CONFIG, contains_slur
from jukebox_client.config.models import LanguageConfig
from jukebox_client.models import JukeBoxClient, MusicRequest, JukeBoxConnectionError
from jukebox_client.views.widgets import LoadingModal
import logging
from .controller import Controller
from jukebox_client.views import HomeView
import shutil


class InfoController(Controller[InfoView]):
    def __init__(self):
        super().__init__(InfoView)

        self.jukebox_client = JukeBoxClient(CONFIG.network.server_ip,
                                            CONFIG.network.server_port)
        self.refresh_docs()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.refresh_docs)
        self.timer.start()

    def connect_view(self): ...

    @QtCore.pyqtSlot()
    def set_selected_language(self):
        language = self.get_language()

        self.view.sub_heading.setText(language.heading_information)

    @QtCore.pyqtSlot()
    def refresh_docs(self):
        try:
            documents = self.jukebox_client.list_documents()

            shutil.rmtree(CONFIG.general.documents_directory)
            os.makedirs(CONFIG.general.documents_directory)
            for doc in documents:
                self.jukebox_client.get_document(doc)
        except JukeBoxConnectionError:
            pass
        finally:
            self.view.list_documents()
