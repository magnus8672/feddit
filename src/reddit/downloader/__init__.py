import requests

HEADERS = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.74 Safari/537.36 "
}


def download(url, params={}, stream=False):
    request = requests.get(url, headers=HEADERS, params=params, stream=stream)
    request.raise_for_status()
    return request
