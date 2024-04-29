import os.path

from PyQt6 import QtCore, QtGui, QtWidgets

from jukebox_client.config import (
    APP_CONFIG_ROOT,
    CLASSICS_SONGS,
    CONFIG,
    CURRENT_CHARTS_SONGS,
    Song,
)
from jukebox_client.config.models import LanguageConfig
from jukebox_client.models import ChartsManager
from jukebox_client.views.widgets import Button, build_accent1_glow_effect

from .helpers import load_colored_svg


class SongRow(QtWidgets.QWidget):
    ICON_SIZE = 48

    def __init__(self, icon: str, description: str, value: str, plays: int = 0):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        icon_label = QtWidgets.QLabel()
        icon_label.setObjectName("SongIconLabel")
        icon_label.setPixmap(load_colored_svg(icon, CONFIG.style.colors.accent1_glow))
        layout.addWidget(icon_label)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        value_label = QtWidgets.QLabel(value)
        value_label.setWordWrap(True)
        value_label.setObjectName("SongValueLabel")
        vbox.addWidget(value_label)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        vbox.addLayout(hbox)

        description_label = QtWidgets.QLabel(description)
        description_label.setObjectName("SongDescriptionLabel")
        hbox.addWidget(description_label)

        hbox.addStretch()

        if plays > 0:
            icon = QtWidgets.QLabel()
            icon.setObjectName("SongIconLabel")
            icon.setPixmap(
                load_colored_svg(
                    CONFIG.icons.charts_plays_icon,
                    CONFIG.style.colors.accent1_glow,
                ),
            )
            hbox.addWidget(icon)

            plays_amount = QtWidgets.QLabel(str(plays))
            plays_amount.setObjectName("SongDescriptionLabel")
            hbox.addWidget(plays_amount)
            layout.addLayout(hbox)

        layout.addLayout(vbox)


class SongWidget(QtWidgets.QGroupBox):
    clicked = QtCore.pyqtSignal()

    def __init__(self, index: int, song: Song, show_plays: bool = False):
        super().__init__()
        self.setObjectName("SongWidget")

        self.index = index
        self.song = song
        self.show_plays = show_plays

        self._build_ui()
        self.setMouseTracking(True)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.song_widget = SongRow(
            CONFIG.icons.song_icon,
            CONFIG.selected_language.classics_song_description,
            self.song.title,
        )
        layout.addWidget(self.song_widget)

        self.artist_widget = SongRow(
            CONFIG.icons.artist_icon,
            CONFIG.selected_language.classics_artist_description,
            self.song.artist,
            plays=self.song.plays,
        )
        layout.addWidget(self.artist_widget)

        self.setStyleSheet(
            "QGroupBox { "
            + f"border:  4px solid {CONFIG.style.colors.accent1_dark};"
            + " }",
        )

    def _set_title(self):
        title = f"# {self.index}"
        self.setTitle(title)

    def event(self, event: QtCore.QEvent) -> bool:
        """Custom event handling to manage hover and click events."""
        if event.type() == QtCore.QEvent.Type.Enter:
            self.setStyleSheet(
                "QGroupBox {"
                + f"border: 4px solid {CONFIG.style.colors.accent1_glow};"
                + "}",
            )
            self.setGraphicsEffect(build_accent1_glow_effect())
        elif event.type() == QtCore.QEvent.Type.Leave:
            self.setStyleSheet(
                "QGroupBox { "
                + f"border:  4px solid {CONFIG.style.colors.accent1_dark};"
                + " }",
            )
            self.setGraphicsEffect(None)
        return super().event(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent | None):  # noqa: N802, inherited
        """Emit the clicked signal when the group box is clicked."""
        self.clicked.emit()
        super().mousePressEvent(event)


class SongsListWidget(QtWidgets.QWidget):
    song_selected = QtCore.pyqtSignal(Song)

    MAX_COLS = 3

    def __init__(self, chart_list: list[Song], show_plays: bool = False):
        super().__init__()
        self.charts = chart_list
        self._song_widgets = []
        self.show_plays = show_plays
        self.setObjectName("SongListWidget")

        self._build_ui()

    def _build_ui(self):
        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.setContentsMargins(48, 32, 48, 32)
        scroll_area = QtWidgets.QScrollArea()
        w = QtWidgets.QWidget()
        w.setObjectName("SongListWidget")
        scroll_area.setWidget(w)

        main_lay.addWidget(scroll_area)

        layout = QtWidgets.QGridLayout(w)
        for index, song in enumerate(self.charts, 1):
            song_widget = SongWidget(index, song, show_plays=self.show_plays)
            song_widget.clicked.connect(self._on_song_selected)
            song_amount = len(self._song_widgets)

            layout.addWidget(
                song_widget,
                song_amount // self.MAX_COLS,
                song_amount % self.MAX_COLS,
            )
            self._song_widgets.append(song_widget)

        scroll_area.setWidgetResizable(True)

    @QtCore.pyqtSlot()
    def _on_song_selected(self):
        sender: SongWidget = self.sender()

        selected_song = sender.song
        self.song_selected.emit(selected_song)


class QuickSelectionDialog(QtWidgets.QDialog):
    MAX_COLS = 3

    def __init__(self, language: LanguageConfig):
        super().__init__()

        self.setObjectName("QuickSelectionDialog")

        charts_path = os.path.join(APP_CONFIG_ROOT, CONFIG.general.charts_file)
        self.charts_manager = ChartsManager(charts_path)

        self._selected_song = None
        self.language = language
        self.songs = CLASSICS_SONGS
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

    def load_charts(self) -> list[Song]:
        return self.charts_manager.get_charts_list()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.tab = QtWidgets.QTabWidget()
        layout.addWidget(self.tab)

        self.classics_widget = SongsListWidget(CLASSICS_SONGS)
        self.classics_widget.song_selected.connect(self._on_song_selected)
        self.tab.addTab(self.classics_widget, "[Classics]")

        self.charts_widget = SongsListWidget(self.load_charts(), show_plays=True)
        self.charts_widget.song_selected.connect(self._on_song_selected)
        self.tab.addTab(self.charts_widget, "[Charts]")

        self.charts_widget = SongsListWidget(CURRENT_CHARTS_SONGS)
        self.charts_widget.song_selected.connect(self._on_song_selected)
        self.tab.addTab(self.charts_widget, "[Radio]")

        close_button = Button("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    @QtCore.pyqtSlot(Song)
    def _on_song_selected(self, song: Song):
        self._selected_song = song
        self.accept()
