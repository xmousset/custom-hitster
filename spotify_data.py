import time

import pandas as pd
from tqdm import tqdm
from spotipy import Spotify, SpotifyClientCredentials, exceptions


class SpotifyAPI:

    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str):
        self.spotify = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET
            )
        )

    def get_playlist_name(self, playlist_id: str) -> str:
        name = self.spotify.playlist(playlist_id, "name")
        if name is None:
            return "Unknown Playlist"
        return name["name"]

    def get_playlist_info(self, playlist_ids: str | list[str]):

        if isinstance(playlist_ids, list):
            all_songs: list[pd.DataFrame] = []
            for playlist_id in playlist_ids:
                df = self.get_playlist_info(playlist_id)
                name = self.get_playlist_name(playlist_id)
                df["playlist_name"] = name
                all_songs.append(df)
            all_df = pd.concat(all_songs, ignore_index=True)
            return all_df

        raw_data = self.spotify.playlist_items(playlist_ids)

        if raw_data is None:
            print(f"Playlist with ID {playlist_ids} not found.")
            return pd.DataFrame()

        songs = []
        total_tracks = raw_data.get("total", None)
        pbar = tqdm(total=total_tracks, desc="Fetching tracks", unit="track")

        while raw_data:
            items = raw_data["items"]
            for item in items:
                track = item["track"]
                if not track:
                    pbar.update(1)
                    continue

                added_by_id = item["added_by"]["id"]
                user = self.spotify.user(added_by_id)
                if user is None:
                    print(f"User with ID {added_by_id} not found.")
                    added_by_name = "Unknown User"
                else:
                    added_by_name = user["display_name"]

                year = int(track["album"]["release_date"][:4])

                songs.append(
                    {
                        "name": track["name"],
                        "artists": [
                            artist["name"] for artist in track["artists"]
                        ],
                        "year": year,
                        "release_date": track["album"]["release_date"],
                        "url": track["external_urls"]["spotify"],
                        "id": track["id"],
                        "added_by_id": added_by_id,
                        "added_by_name": added_by_name,
                    }
                )
                pbar.update(1)

            next_data = SpotifyAPI.safe_api_call(self.spotify.next, raw_data)
            raw_data = next_data if next_data else None

        pbar.close()
        return pd.DataFrame(songs)

    @staticmethod
    def safe_api_call(api_call, *args, **kwargs):
        while True:
            try:
                return api_call(*args, **kwargs)
            except exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get("Retry-After", 1))
                    time.sleep(retry_after)
                else:
                    raise
