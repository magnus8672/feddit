import time
from datetime import datetime

from requests import HTTPError

from config.parser import get_config
from filesystem.file import writer
from reddit.downloader import download
from video.process import merge

MODE = "wb"
DATE_FORMAT = "%d%m%Y%H%M%S"
# TODO: delay should be an option in feddit.ini
DELAY = 2


def create_all(videos_url):
    for url in videos_url:
        create(url)
        time.sleep(DELAY)


def create(url):
    config = get_config()
    date = datetime.now().strftime(DATE_FORMAT)
    root_location = config["rootlocation"]
    target_location = config["targetlocation"]
    video_id = url.split("/")[3]

    audio_url = f"https://v.redd.it/{video_id}/DASH_audio.mp4"
    video_name = f"{root_location}video{date}.mp4"
    audio_name = f"{root_location}audio{date}.mp3"
    save(url, video_name)
    save(audio_url, audio_name)
    filename = f"{target_location}redditvideo{date}.mp4"
    merge(video_name, audio_name, filename)


def save(url, filename):
    try:
        file = download(url, stream=True)
        writer(file.content, filename, MODE)
    except (HTTPError, OSError) as error:
        print("there was an error trying download the file" + str(error))
