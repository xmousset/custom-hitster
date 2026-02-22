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
    assert client_id is not None, "CLIENT_ID must be set in the .env file"
    assert (
        client_secret is not None
    ), "CLIENT_SECRET must be set in the .env file"
    spotify_id = {
        "CLIENT_ID": client_id,
        "CLIENT_SECRET": client_secret,
    }
    return spotify_id


def get_deck_from_playlist(
    playlist_id: str, output_path: str | Path | None = None
):
    """Fetch playlist data from Spotify and save dataset to CSV.
    Returns a HitsterDeck object with the playlist data."""
    sp_api = SpotifyAPI(**get_spotify_id())
    name = sp_api.get_playlist_name(playlist_id)
    df = sp_api.get_playlist_info(playlist_id)

    deck = HitsterDeck(name=name)
    deck.data = df
    if isinstance(output_path, str):
        output_path = Path(output_path)

    deck.save_to_csv(file_path=output_path)

    return deck


def get_deck_from_csv(file_path: str | Path):
    """Load playlist data from a CSV file.
    Returns a HitsterDeck object with the playlist data."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    name = file_path.stem
    deck = HitsterDeck(name=name)
    deck.load_from_csv(file_path=file_path)

    return deck


if __name__ == "__main__":
    playlist = "spotify_playlist_URI_goes_here"

    deck = get_deck_from_playlist(playlist, "your_playlist.csv")
    # deck = get_deck_from_csv("your_playlist.csv")

    deck.analyse_dataframe()

    deck.create_hitster()
