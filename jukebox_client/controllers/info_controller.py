import os
import shutil

from PyQt6 import QtCore

from jukebox_client.config import CONFIG
from jukebox_client.models import JukeBoxClient, JukeBoxConnectionError
from jukebox_client.views import InfoView

from .controller import Controller


class InfoController(Controller[InfoView]):
    def __init__(self):
        super().__init__(InfoView)

        self.jukebox_client = JukeBoxClient(
            CONFIG.network.server_ip,
            CONFIG.network.server_port,
        )
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
