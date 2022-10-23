from downloader import download
from config.parser import getconfig

DEFAULT_LIMIT = 100


def getjson():
    config = getconfig()
    url = f"{config['baseUrl']}.json"
    params = {}
    params.setdefault('limit', DEFAULT_LIMIT)
    response = download(url, params)
    return response.json()

