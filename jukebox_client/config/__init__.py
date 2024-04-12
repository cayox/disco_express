import os.path
import re
import tomllib
from .models import Config, Song
import csv

ASSETS = os.path.join(os.getcwd(), "assets")

root = os.path.dirname(__file__)
config = os.path.join(root, "../../assets/config.toml")
with open(config, "rb") as f:
    CONFIG = Config(**tomllib.load(f))

slurs_file = os.path.join(os.getcwd(), CONFIG.general.slurs_file)
with open(slurs_file, "rb") as f:
    SLURS = f.readlines()
    SLURS = [slur.decode().replace("\n", "").lower() for slur in SLURS]


def contains_slur(text: str) -> bool:
    words = text.lower().split(" ")

    return any(word in SLURS for word in words)

def load_songs_from_csv(file_path: str) -> list[Song]:
    songs = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:
            song = Song(title=row[0], artist=row[1])
            songs.append(song)
    return songs

# Example usage
quick_selecton_file = os.path.join(os.getcwd(), CONFIG.general.quick_selection_file)
QUICK_SELECTION_SONGS = load_songs_from_csv(quick_selecton_file)
