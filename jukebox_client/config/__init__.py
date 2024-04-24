import csv
import os.path
import re
import tomllib

from .models import Config, Song

ASSETS = os.path.join(os.getcwd(), "assets")

root = os.path.dirname(__file__)
config = os.path.join(root, "../../assets/config.toml")
with open(config, "rb") as f:
    toml = tomllib.load(f)
    CONFIG = Config(**toml)

slurs_file = os.path.join(os.getcwd(), CONFIG.general.slurs_file)
with open(slurs_file, "rb") as f:
    SLURS = f.readlines()
    SLURS = [slur.decode().replace("\n", "").lower() for slur in SLURS]


def contains_slur(text: str) -> bool:
    words = text.lower().split(" ")

    return any(word in SLURS for word in words)


def load_songs_from_csv(file_path: str) -> list[Song]:
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


classics_file = os.path.join(os.getcwd(), CONFIG.general.classics_file)
CLASSICS_SONGS = load_songs_from_csv(classics_file)

current_charts_file = os.path.join(os.getcwd(), CONFIG.general.current_charts)
CURRENT_CHARTS_SONGS = load_songs_from_csv(current_charts_file)
