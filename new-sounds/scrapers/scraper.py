import aiohttp
import asyncio
import json
import logging
import os

import pandas as pd


class WebScraper(object):
    def __init__(self, urls):
        self.urls = urls
        # Global Place To Store The Data:
        self.all_data = []
        self.master_dict = {}
        # Run The Scraper:
        asyncio.run(self.main())

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                return json.loads(text), url
        except Exception as e:
            print(str(e))
            logging.error(str(e))

    async def main(self):
        tasks = []
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        connector = aiohttp.TCPConnector(limit=30)
        async with aiohttp.ClientSession(
            headers=headers, connector=connector
        ) as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            json_and_url = await asyncio.gather(*tasks)
            self.all_data.extend(json_and_url)

            all_data = []
            # Storing the raw HTML data.
            for json, url in json_and_url:
                if json is not None:
                    day_data = []
                    # Process the data here
                    for events in json["events"]:
                        for playlists in events["playlists"]:
                            for played in playlists["played"]:
                                try:
                                    song_info = played["info"]
                                    artist_name = (
                                        song_info.get("composer")
                                        or song_info.get("ensemble")
                                    ).get("name")
                                    start_time = played["iso_start_time"]
                                    song_name = song_info["title"]
                                    uid = song_info.get("mm_uid")
                                    day_data.append(
                                        {
                                            "artist": artist_name,
                                            "start_time": start_time,
                                            "title": song_name,
                                            "uid": uid,
                                        }
                                    )
                                except:
                                    logging.error(
                                        f"Failed to scrape in {url}, {played}"
                                    )
                    *_, year, month, day = url.split("/")
                    os.makedirs(f"data/{year}/{month}/{day}", exist_ok=True)
                    dataframe = pd.DataFrame(day_data)
                    dataframe.to_csv(
                        "data/{}/{}/{}/song_info.csv".format(year, month, day),
                        index=False,
                    )
                    all_data.extend(day_data)
                    self.master_dict[url] = {"Raw Html": json}
                else:
                    continue

            all_data = pd.DataFrame(all_data)
            all_data.to_csv("../data/all_songs_data.csv", index=False)

            unique_songs = all_data.drop_duplicates(subset="uid")
            unique_songs.index = unique_songs.uid
            unique_songs = unique_songs.drop(columns=["uid", "start_time"])
            unique_songs.to_csv("../data/unique_songs.csv", index=True)


class DateURLFactory:
    def __init__(
        self,
        start_date,
        end_date,
        url_format="https://api.wnyc.org/api/v1/playlist-daily/q2/{year}/{month}/{day}/",
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.url_format = url_format

    def get_urls(self):
        url_list = []
        for date in pd.date_range(self.start_date, self.end_date):
            year = date.strftime("%Y")
            month = date.strftime("%b").lower()
            day = date.strftime("%d")
            url = self.url_format.format(year=year, month=month, day=day)
            url_list.append(url)
        return url_list


if __name__ == "__main__":
    start_date = "2022-01-01"
    end_date = "2022-01-31"
    url_format = "https://api.wnyc.org/api/v1/playlist-daily/q2/{year}/{month}/{day}/"
    date_url_factory = DateURLFactory(start_date, end_date, url_format)
    urls = date_url_factory.get_urls()
    web_scraper = WebScraper(urls)
