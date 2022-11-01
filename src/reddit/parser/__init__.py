import json

from reddit.downloader import download
from config.parser import get_config

DEFAULT_LIMIT = 100


def get_json():
    config = get_config()
    url = f"{config['baseUrl']}.json"
    params = {}
    params.setdefault('limit', DEFAULT_LIMIT)
    response = download(url, params)
    return response.json()


def get_videos(json_text):
    loaded_json = json.loads(json_text)
    listed_videos = loaded_json['data']['children']
    videos = [video['data']['secure_media']['reddit_video']['fallback_url'] for video in listed_videos
              if (check_video(video)) is True]
    return videos


def check_video(video):
    try:
        video['data']['secure_media']['reddit_video']['fallback_url']
        return True
    except KeyError:
        # TODO: crear logger con un método para los videos
        return False
