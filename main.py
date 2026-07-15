import os
from pathlib import Path

from dotenv import load_dotenv

from hitster_deck import HitsterDeck
from spotify_data import SpotifyAPI


def get_spotify_id():
    """Load Spotify API credentials from .env file."""
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    msg = "must be set in the .env file"
    assert client_id is not None, f"CLIENT_ID {msg}"
    assert client_secret is not None, f"CLIENT_SECRET {msg}"
    spotify_id = {
        "CLIENT_ID": client_id,
        "CLIENT_SECRET": client_secret,
    }
    return spotify_id


def create_csv_from_playlist(
    playlist_id: str,
    output_path: str | Path | None = None,
):
    """Fetch playlist data from Spotify and save dataset to CSV.
    Returns a HitsterDeck object with the playlist data."""
    if isinstance(output_path, str):
        if not output_path.endswith(".csv"):
            output_path += ".csv"
        output_path = Path(output_path)

    sp_api = SpotifyAPI(**get_spotify_id())
    name = sp_api.get_playlist_name(playlist_id)
    df = sp_api.get_playlist_info(playlist_id)

    deck = HitsterDeck(name=name)
    deck.data = df
    deck.save_to_csv(output_path)

    return deck


def create_deck_from_csv(file_path: str | Path):
    """Load playlist data from a CSV file.
    Returns a HitsterDeck object with the playlist data."""
    if isinstance(file_path, str):
        if not file_path.endswith(".csv"):
            file_path += ".csv"
        file_path = Path(file_path)

    deck = HitsterDeck(file_path.stem)
    deck.load_from_csv(file_path)
    return deck


if __name__ == "__main__":
    PLAYLIST = "spotify_playlist_URI_goes_here"
    CSV_FILE = "output_data.csv"

    deck = create_csv_from_playlist(PLAYLIST, CSV_FILE)
    deck = create_deck_from_csv(CSV_FILE)

    # deck.check_data_integrity()  # check for missing values and duplicates
    # deck.analyse_dataframe()  # histogram of the number of songs per year
    deck.create_hitster()
