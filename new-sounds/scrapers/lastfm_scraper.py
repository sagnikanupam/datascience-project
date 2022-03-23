import os
import pandas as pd
import pylast


class LastFMScraper:
    def __init__(self, titles, artists, network) -> None:
        self.titles = titles
        self.artists = artists
        self.network = network

    def scrape(self):
        all_tags = []
        for artist, title in zip(self.artists, self.titles):
            track = self.network.get_track(artist, title)
            tags = track.get_top_tags()
            all_tags.append(tags)
        return all_tags


if __name__ == "__main__":
    unique_song_data = pd.read_csv("../data/unique_songs.csv")
    network = pylast.LastFMNetwork(
        api_key=os.environ.get("LASTFM_API_KEY"),
        api_secret=os.environ.get("LASTFM_API_SECRET"),
        username=os.environ.get("LASTFM_USERNAME"),
        password_hash=os.environ.get("LASTFM_PASSWORD_HASH"),
    )
    scraper = LastFMScraper(
        titles=unique_song_data["title"],
        artists=unique_song_data["artist"],
        network=network,
    )
    tags = scraper.scrape()
    unique_song_data["tags"] = tags
    unique_song_data.to_csv("../data/unique_songs_with_lastfm_tags.csv", index=False)
