import os.path
import tomllib
from .models import Config

root = os.path.dirname(__file__)
config = os.path.join(root, "config.toml")
with open(config, "rb") as f:
    CONFIG = Config(**tomllib.load(f))

slurs_german = os.path.join(root, "slurs_german.txt")
with open(config, "rb") as f:
    SLURS_GERMAN = f.readlines()

slurs_english = os.path.join(root, "slurs_english.txt")
with open(config, "rb") as f:
    SLURS_ENGLISH = f.readlines()


def is_slur(text: str) -> bool:
    return any(str(slur) in text for slur in SLURS_ENGLISH + SLURS_GERMAN)
