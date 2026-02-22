from pathlib import Path

import typst
import pandas as pd
import plotly.express as px


def clean_string(s: str) -> str:
    """Clean a string by removing brackets and quotes. Used for the artists
    column."""
    s = s.replace("['", "").replace("']", "")
    s = s.replace("', '", ", ")
    return s


class HitsterDeck:

    def __init__(self, name: str) -> None:
        self.data: pd.DataFrame = pd.DataFrame()
        self.name = name
        self.cwd = Path(__file__).parent

    def save_to_csv(self, file_path: Path | None = None):
        if self.data is None:
            raise ValueError("Set the data attribute before saving.")
        if file_path is None:
            file_path = self.cwd / (self.name + ".csv")
        file_path.parent.mkdir(exist_ok=True, parents=True)
        self.data.to_csv(file_path, index=False)

    def load_from_csv(self, file_path: Path | None = None):
        if file_path is None:
            file_path = self.cwd / (self.name + ".csv")
        self.data = pd.concat(
            [self.data, pd.read_csv(file_path)], ignore_index=True
        )
        return self.data

    def analyse_dataframe(self):
        if self.data.empty:
            raise ValueError("Set the data attribute before analysing.")
        year_counts = self.data["year"].value_counts().sort_index()

        fig = px.bar(
            x=year_counts.index,
            y=year_counts.values,
            labels={"x": "Année de sortie", "y": "Nombre de musiques"},
            title=f"Total : {year_counts.sum()} musiques",
        )
        fig.update_layout(xaxis=dict(tickmode="linear", dtick=5))
        fig.write_image(self.cwd / (self.name + " - analysis.pdf"))

    def create_hitster(self):
        if self.data.empty:
            raise ValueError(
                "Set the data attribute before creating the hitster."
            )
        typst_template = self.cwd / "hitster_card.typ"
        output_path = self.cwd / (self.name + " - hitster deck.pdf")
        output_path.parent.mkdir(exist_ok=True, parents=True)

        nb_tracks = len(self.data)
        sys_inputs = {}
        sys_inputs["nb_tracks"] = str(nb_tracks)
        for track_id in range(nb_tracks):
            for col in self.data.columns:
                if col == "artists":
                    value = clean_string(self.data[col].iloc[track_id])
                else:
                    value = str(self.data[col].iloc[track_id])
                sys_inputs[col + "_" + str(track_id)] = value

        print(f"Creating hitster deck with {nb_tracks} tracks...")
        typst.compile(
            input=str(typst_template),
            output=str(output_path),
            format="pdf",
            ppi=600.0,
            sys_inputs=sys_inputs,
        )
        print("Hitster deck created successfully.")
        print(f"Saved to {output_path}")
