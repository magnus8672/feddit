import json
import logging

from reddit.downloader import download
from config.parser import get_config

DEFAULT_LIMIT = 100


def get_json(params={}):
    config = get_config()
    url = f"{config['baseurl']}.json"
    params.setdefault('limit', DEFAULT_LIMIT)
    response = download(url, params)
    return response.json()


def extract_video_url(parsed_json):
    videos = [video['data']['secure_media']['reddit_video']['fallback_url'] for video in parsed_json
              if (check_video(video)) is True]
    return videos


def check_video(video):
    try:
        video['data']['secure_media']['reddit_video']['fallback_url']
        return True
    except (KeyError, TypeError):
        logging.error("A child object in json did not contain a video URL. Video Type was: %s", video)
        return False


def extract_next_index(loaded_json):
    if loaded_json['data']['after'] is None:
        return ""

    return loaded_json['data']['after']
