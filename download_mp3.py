from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl as yd
import pandas as pd
import os


def scrape_vid_id(query):
    print(f"Getting video id for: {query}")
    BASIC = "https://www.youtube.com/results?search_query="
    URL = BASIC + query
    URL.replace(" ", "+")
    page = requests.get(URL)
    session = HTMLSession()
    response = session.get(URL)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "html.parser")

    results = soup.find("a", id="video-title")
    return results["href"].split("/watch?v=")[1]


def download_mp4_from_titles(los):
    ids = []
    for index, item in enumerate(los):
        vid_id = scrape_vid_id(item)
        ids += [vid_id]
    print("Downloading videos...")
    download_mp4_from_ids(ids)


def download_mp4_from_ids(lov):
    SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print("Directory already exists")
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": SAVE_PATH + "/%(title)s.%(ext)s",
    }
    with yd.YoutubeDL(ydl_opts) as ydl:
        ydl.download(lov)


def __main__():
    data = pd.read_csv("songs.csv")
    data = data["column"].split("/watch?v=")[1]
    print(f"Found {len(data)} songs")
    download_mp4_from_titles(data[0:1])


__main__()
