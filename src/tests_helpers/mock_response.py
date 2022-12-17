import json
from requests import Response


class MockResponse(Response):
    def __init__(self,
                 url='http://example.com',
                 headers={'Content-Type':'text/html; charset=UTF-8'},
                 status_code=200,
                 reason='Success',
                 _content='Some html goes here',
                 json_=None,
                 encoding='UTF-8'
                 ):
        self.url = url
        self.headers = headers

        if json_ and headers['Content-Type'] == 'application/json':
            self._content = json.dumps(json_).encode(encoding)
        else:
            self._content = _content.encode(encoding)

        self.status_code = status_code
        self.reason = reason
        self.encoding = encoding

