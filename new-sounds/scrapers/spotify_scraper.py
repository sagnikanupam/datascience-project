import pandas as pd
import spotipy
from tqdm.auto import tqdm
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyScraper:
    def __init__(self, data: pd.DataFrame, network: spotipy.Spotify) -> None:
        self.network = network
        self.data = data

    def scrape(self) -> pd.DataFrame:
        tags = []
        items, albums, artists = [], [], []
        missing_track = 0
        missing_artist = 0
        for artist, title in tqdm(
            zip(self.data.artist, self.data.title), total=len(self.data)
        ):
            tracks = self.network.search(
                q="artist:" + str(artist) + " track:" + str(title),
                type="track",
            )
            if tracks["tracks"]["total"] == 0:
                missing_track += 1
                tqdm.write(f"No tracks found for {artist} - {title}")
                items.append(None)
                albums.append(None)
                # Try to scrape genres from the artist
                artist_data = self.network.search(
                    q="artist:" + str(artist),
                    type="artist",
                )
                if artist_data["artists"]["total"] == 0:
                    missing_artist += 1
                    tqdm.write(f"No artists found for {artist}")
                    artists.append(None)
                    tags.append([])
                else:
                    artists.append(artist_data["artists"]["items"][0]["uri"])
                    tags.append(artist_data["artists"]["items"][0]["genres"])
                continue
            item_uri = tracks["tracks"]["items"][0]["uri"]
            album_uri = tracks["tracks"]["items"][0]["album"]["uri"]
            artist_uri = tracks["tracks"]["items"][0]["artists"][0]["uri"]

            items.append(item_uri)
            albums.append(album_uri)
            artists.append(artist_uri)

            # Spotify doesn't allow us to get the tags for a track, so we have to
            # get the album tags, and if that is unavailable, the artist tags.
            album = self.network.album(album_uri)
            if len(album["genres"]):
                tags.append(album["genres"])
            else:
                artist = self.network.artist(artist_uri)
                tags.append(artist["genres"])

        extra_columns = pd.DataFrame(
            {
                "artist_uri": artists,
                "album_uri": albums,
                "item_uri": items,
                "tags": tags,
            }
        )
        self.data = pd.concat([self.data, extra_columns], axis=1)
        print(missing_artist, missing_track)
        return self.data


if __name__ == "__main__":
    unique_song_data = pd.read_csv("../data/unique_songs.csv")
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    scraper = SpotifyScraper(
        data=unique_song_data,
        network=spotify,
    )
    refreshed_data = scraper.scrape()
    print(refreshed_data.head())
    refreshed_data.to_csv("../data/unique_songs_with_spotify_tags.csv")
