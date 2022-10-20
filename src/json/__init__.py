from downloader import download
from config import getconfig


def getjson(params={}):
    config = getconfig()
    url = f"{config['baseURL']}.json"
    return download(url, params)

