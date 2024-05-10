import csv
import os.path
import shutil
import sys
import tomllib

from .models import Config, Song


def get_application_path() -> str:
    """Return the path of the application."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # noqa: SLF001
    return os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__))


APP_CONFIG_ROOT = os.path.expanduser("~/disco_express")

ASSETS = os.path.join(get_application_path(), "assets")


def checkout_files():
    """Check if necessary files are in APP_CONFIG_ROOT and copy them there if not."""
    os.makedirs(APP_CONFIG_ROOT, exist_ok=True)

    dirs_to_checkout = ["img", "data", "icons"]
    for checkout_dir in dirs_to_checkout:
        dst = os.path.join(APP_CONFIG_ROOT, checkout_dir)
        if not os.path.isdir(dst):
            src = os.path.join(ASSETS, checkout_dir)
            shutil.copytree(src, dst)

    config_path = os.path.join(APP_CONFIG_ROOT, "config.toml")
    if not os.path.isfile(config_path):
        src = os.path.join(ASSETS, "config.toml")
        shutil.copy(src, APP_CONFIG_ROOT)


checkout_files()

config = os.path.join(APP_CONFIG_ROOT, "config.toml")
with open(config, "rb") as f:
    toml = tomllib.load(f)
    CONFIG = Config(**toml)

slurs_file = os.path.join(APP_CONFIG_ROOT, CONFIG.general.slurs_file)
with open(slurs_file, "rb") as f:
    SLURS = f.readlines()
    SLURS = [slur.decode().replace("\n", "").lower() for slur in SLURS]


def contains_slur(text: str) -> bool:
    """Function to check if a text contains a slur."""
    words = text.lower().split(" ")

    return any(word in SLURS for word in words)


def load_songs_from_csv(file_path: str) -> list[Song]:
    """Function to load the songs from a csv file."""
    songs = []
    with open(file_path, newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip the header
        for row in reader:
            song = Song(title=row[0], artist=row[1], plays=0)
            if len(row) > 2:  # noqa: PLR2004
                song.plays = row[2]
            songs.append(song)
    return songs


classics_file = os.path.join(APP_CONFIG_ROOT, CONFIG.general.classics_file)
CLASSICS_SONGS = load_songs_from_csv(classics_file)

current_charts_file = os.path.join(APP_CONFIG_ROOT, CONFIG.general.current_charts)
CURRENT_CHARTS_SONGS = load_songs_from_csv(current_charts_file)
