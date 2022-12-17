import logging
import os.path
from shutil import copy2
import time
from datetime import datetime

from requests import HTTPError

from config.parser import get_config
from filesystem.file import writer
from reddit.downloader import download
from video.process import merge

MODE = "wb"
DATE_FORMAT = "%d%m%Y%H%M%S"


def create_all(videos_url):
    config = get_config()
    delay = int(config["delay"])

    for url in videos_url:
        create(url)
        time.sleep(delay)


def create(url):
    config = get_config()
    date = datetime.now().strftime(DATE_FORMAT)
    root_location = config["rootlocation"]
    target_location = config["targetlocation"]
    video_id = url.split("/")[3]
    audio_url = f"https://v.redd.it/{video_id}/DASH_audio.mp4"
    video_name = f"{root_location}video{date}.mp4"
    audio_name = f"{root_location}audio{date}.mp3"

    logging.info("Download Video and audio from: " + url)
    save(url, video_name)
    save(audio_url, audio_name)
    filename = f"{target_location}redditvideo{date}.mp4"

    if os.path.exists(audio_name):
        merge(video_name, audio_name, filename)
    else:
        copy2(video_name, filename)


def save(url, filename):
    try:
        file = download(url, stream=True)
        writer(file.content, filename, MODE)
    except (HTTPError, OSError) as error:
        print("there was an error trying download the file" + str(error))
