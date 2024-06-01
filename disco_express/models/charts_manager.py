import os

import pandas as pd

from disco_express.config.models import Song

HEADER = ["Title", "Artist", "Plays"]


class ChartsManager:
    """A manager managing charts with their respective plays and sorting them accordingly.

    Args:
        charts_file: the file the charts should be saved/loaded from.
        charts_threshold: the minimum amount of plays needed to be in the charts.
    """

    def __init__(self, charts_file: str, charts_threshold: int = 0):
        self.charts_file = charts_file
        self.charts_threshold = charts_threshold

        if os.path.isfile(self.charts_file):
            self.charts = self.load_charts()
        else:
            self.charts = pd.DataFrame(columns=HEADER)

    def get_charts_list(self) -> list[Song]:
        """Method to retrieve the chars as a list of Songs."""
        charts = self.charts[self.charts["Plays"] >= self.charts_threshold].sort_values(
            "Plays",
            ascending=False,
        )

        out = []
        for _, chart in charts.iterrows():
            out.append(
                Song(
                    title=chart["Title"],
                    artist=chart["Artist"],
                    plays=chart["Plays"],
                ),
            )

        return out

    def load_charts(self) -> pd.DataFrame:
        """Method to load the charts' database."""
        return pd.read_csv(self.charts_file, sep=";", header=0)

    def add_song(self, song: Song):
        """Method to add a song into the charts' database.

        Args:
            song: the song to add
        """
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
