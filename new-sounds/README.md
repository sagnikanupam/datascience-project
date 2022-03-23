# Genre Bias in New Sounds

## Background
I am really loving this new radio station in New York, called New Sounds – like, I am 
practically obsessed! And as I am listening more and more to their livestream on the 
[website](https://newsounds.org), I have started to get this feeling that the genre of 
music they play during the morning (7-9 AM) is significantly different than the genre of
 music they play during the afternoon (4-6 PM). How do I confirm or deny this hypothesis?

You can access the livestream and playlist music history on this page: ​​
https://www.newsounds.org/livestream . Can you build a model that examines my hypothesis
 with data from somewhere between 1-6 months, and comes up with an answer?

## For data science intern applicants
You can use the data that we have already scraped for the month of January, located in
the data folder. Use the `unique_songs_with_single_tags.csv` to build your model.

## Questions to think about (doesn’t need to be in the writeup.)
* How do you get the music data for New Sounds radio in a format you can process it?
* How do you get the associated genres for those songs? How do you deal with missing data, as in, what if on the common sources of data you are looking at, the song doesn't even have a genre?
* What is the hypothesis, formally put?

## Deliverable
We want you to make a github repo with the code that you used to scrape the data. 
You can start by just cloning this repo.
Alongside, we would like you to make a report, which can be either a writeup, slides, or
 even a python notebook with some visualizations that show the result you have found.

## Using our code
You can install all the necessary packages using `poetry`. Just install Python version 
3.8 or higher, install `poetry` package with `pip install poetry`, and do `poetry install`
in this directory.

If you are collecting more data, use the sample dotenv, get all the necessary API keys,
and then `source .env` to load the environment variables.

## Helpful links
* **If you are collecting your own data** You can find the playlists in the livestream link; is there a way to get the data in a JSON somehow from the page, without having to parse the page HTML?
* Spotify API: https://developer.spotify.com/documentation/web-api/guides/ and python library: https://github.com/plamere/spotipy
* Last FM API: https://www.last.fm/api/show/track.getTopTags and python library https://github.com/pylast/pylast


