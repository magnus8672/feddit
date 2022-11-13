import os

from config.parser import get_config


def merge(video, audio, filename):
    config = get_config()
    ffmpeg_location = config['ffmpeglocation']
    command = f"{ffmpeg_location}ffmpeg.exe -i {video} -i {audio} -c copy {filename}"
    os.system(command)
