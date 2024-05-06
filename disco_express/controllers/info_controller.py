import os
import shutil

from PyQt6 import QtCore

from disco_express.config import APP_CONFIG_ROOT, CONFIG
from disco_express.models import JukeBoxClient, JukeBoxConnectionError
from disco_express.views import InfoView

from .controller import Controller


class InfoController(Controller[InfoView]):
    def __init__(self):
        super().__init__(InfoView)

        self._document_cache = []

        self.jukebox_client = JukeBoxClient(
            CONFIG.network.server_ip,
            CONFIG.network.server_port,
        )
        self.refresh_docs()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10000)
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
            if documents == self._document_cache:
                return

            docs_dir = os.path.join(APP_CONFIG_ROOT, CONFIG.general.documents_directory)
            if os.path.isdir(docs_dir):
                shutil.rmtree(docs_dir)
            os.makedirs(docs_dir)
            for doc in documents:
                self.jukebox_client.get_document(doc, docs_dir)

            self._document_cache = documents
        except JukeBoxConnectionError:
            pass
        finally:
            self.view.list_documents()
