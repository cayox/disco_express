import os.path

from PyQt6 import QtWidgets, QtCore, QtGui, QtSvg
from jukebox_client.config import QUICK_SELECTION_SONGS, Song, ASSETS, CONFIG
from jukebox_client.config.models import LanguageConfig
from jukebox_client.views.widgets import Button


class SongRow(QtWidgets.QWidget):
    ICON_SIZE = 48

    def __init__(self, icon: str, description: str, value: str):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(self.load_colored_svg(icon, CONFIG.colors.icon_color))
        layout.addWidget(icon_label)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        value_label = QtWidgets.QLabel(value)
        value_label.setWordWrap(True)
        value_label.setObjectName("SongValueLabel")
        vbox.addWidget(value_label)

        description_label = QtWidgets.QLabel(description)
        description_label.setObjectName("SongDescriptionLabel")
        vbox.addWidget(description_label)

        layout.addLayout(vbox)

    def load_colored_svg(self, svg_path: str, color: str) -> QtGui.QPixmap:
        """Load and color an SVG, returning a QPixmap."""
        # Read SVG data
        with open(svg_path, "rb") as file:
            svg_data = file.read()

        # Replace color in SVG
        svg_data = svg_data.replace(b'fill="#000000"', f'fill="{color}"'.encode())

        # Render the modified SVG
        svg_renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data))
        image = QtGui.QPixmap(QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))  # Set the size as needed
        image.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(image)
        svg_renderer.render(painter)
        painter.end()

        return image


class SongWidget(QtWidgets.QGroupBox):
    clicked = QtCore.pyqtSignal()

    def __init__(self, index: int, song: Song, language: LanguageConfig):
        super().__init__()
        self.setObjectName("SongWidget")

        self.index = index
        self.song = song
        self.language = language

        self._build_ui()
        self.setMouseTracking(True)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        song_icon = os.path.join(os.getcwd(), CONFIG.general.song_icon)
        self.song_widget = SongRow(song_icon, self.language.quick_selection_song_description, self.song.title)
        layout.addWidget(self.song_widget)

        artist_icon = os.path.join(os.getcwd(), CONFIG.general.artist_icon)
        self.artist_widget = SongRow(artist_icon, self.language.quick_selection_artist_description, self.song.artist)
        layout.addWidget(self.artist_widget)



    def _set_title(self):
        title = f"# {self.index}"
        self.setTitle(title)

    def event(self, event: QtCore.QEvent) -> bool:
        """Custom event handling to manage hover and click events."""
        if event.type() == QtCore.QEvent.Type.Enter:
            self.setStyleSheet(f"QGroupBox{{background-color: {CONFIG.colors.highlight};}}")
        elif event.type() == QtCore.QEvent.Type.Leave:
            self.setStyleSheet(f"QGroupBox{{background-color: {CONFIG.colors.accent};}}")
        return super().event(event)

    def mousePressEvent(self, event):
        """Emit the clicked signal when the group box is clicked."""
        self.clicked.emit()
        return super().mousePressEvent(event)


class QuickSelectionDialog(QtWidgets.QDialog):
    MAX_COLS = 3

    def __init__(self, language: LanguageConfig):
        super().__init__()

        self.setObjectName("QuickSelectionDialog")

        self._selected_song = None
        self.language = language
        self.songs = QUICK_SELECTION_SONGS
        self._song_widgets = []

        self.setFixedWidth(1200)
        self.setMinimumHeight(800)

        self._build_ui()

        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(CONFIG.general.auto_close_time * 1000)

    @property
    def selected_song(self) -> Song | None:
        return self._selected_song

    def _build_ui(self):
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.setContentsMargins(48, 32, 48, 32)
        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        scroll_area.setWidget(w)

        main_lay.addWidget(scroll_area)

        layout = QtWidgets.QGridLayout(w)
        for index, song in enumerate(self.songs, 1):
            song_widget = SongWidget(index, song, self.language)
            song_widget.clicked.connect(self._on_song_selected)
            song_amount = len(self._song_widgets)

            layout.addWidget(song_widget, song_amount // self.MAX_COLS, song_amount % self.MAX_COLS)
            self._song_widgets.append(song_widget)

        close_button = Button("Close")
        close_button.clicked.connect(self.close)
        main_lay.addWidget(close_button)

        scroll_area.setWidgetResizable(True)

    @QtCore.pyqtSlot()
    def _on_song_selected(self):
        sender: SongWidget = self.sender()

        self._selected_song = sender.song
        self.accept()



