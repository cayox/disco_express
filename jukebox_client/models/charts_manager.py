import os
from jukebox_client.config import CONFIG, load_songs_from_csv
from jukebox_client.config.models import Song
import pandas as pd

HEADER = ["Title", "Artist", "Plays"]


class ChartsManager:
    def __init__(self, charts_file: str):
        self.charts_file = charts_file

        if os.path.isfile(self.charts_file):
            self.charts = self.load_charts()
        else:
            self.charts = pd.DataFrame(columns=HEADER)

    def get_charts_list(self) -> list[Song]:
        charts = self.charts.sort_values("Plays", ascending=False)

        out = []
        for _, chart in charts.iterrows():
            out.append(
                Song(title=chart["Title"], artist=chart["Artist"], plays=chart["Plays"])
            )

        return out

    def load_charts(self) -> pd.DataFrame:
        return pd.read_csv(self.charts_file, sep=";", header=0)

    def add_song(self, song: Song):
        titles = [title.strip().lower() for title in self.charts["Title"].values]

        if song.title.strip().lower() in titles:
            self.charts.loc[
                (self.charts["Title"].str.contains(song.title, case=False))
                & (self.charts["Artist"].str.contains(song.artist, case=False)),
                "Plays",
            ] += 1
        else:
            data = {"Title": song.title, "Artist": song.artist, "Plays": 1}
            new_row = pd.DataFrame(data, columns=data.keys(), index=[0])
            self.charts = pd.concat([self.charts, new_row], ignore_index=True)

        self.charts.to_csv(self.charts_file, sep=";", index=False)
