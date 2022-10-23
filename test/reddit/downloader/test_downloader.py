from unittest import TestCase, mock

import requests.exceptions

from helper.mock_response import MockResponse
from reddit.downloader import download


class Test(TestCase):
    @mock.patch('reddit.downloader.requests.get')
    def test_download_is_successfull(self, mocked):
        """
        GIVEN an url and a parameter dictionary
        WHEN download a file
        THEN it should return a file
        """
        mocked.return_value = MockResponse()
        url = ""
        params = {}
        request = download(url, params)
        self.assertTrue(request.ok)

    @mock.patch('reddit.downloader.requests.get')
    def test_download_raise_exception(self, mocked):
        """
        GIVEN an url and a parameter dictionary
        WHEN download a file
        THEN it should raise an exception
        """
        with self.assertRaises(Exception):
            mocked.side_effect = requests.exceptions.ConnectionError()
            url = ""
            params = {}
            download(url, params)
