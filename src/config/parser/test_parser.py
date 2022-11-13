from unittest import mock, TestCase

from config.parser import get_config
from tests_helpers.fake_file import fake_ini_file


class TestConfigParser(TestCase):
    @mock.patch('config.reader.configparser.open')
    def test_empty_getconfig(self, mock_open):
        """
        GIVEN an empty ini file
        WHEN is read
        THEN it should return an empty dictionary
        """
        mock_open.return_value = fake_ini_file()

        config = get_config()

        self.assertTrue(type(config) is dict)

    @mock.patch('config.reader.configparser.open')
    def test_getconfig_with_content(self, mock_open):
        """
        GIVEN an empty ini file
        WHEN is read
        THEN it should return an empty dictionary
        """
        key = "test"
        content = f"{key}=yes"
        mock_open.return_value = fake_ini_file(content)

        config = get_config()

        self.assertTrue(key in config)
