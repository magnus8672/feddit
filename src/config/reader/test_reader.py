from unittest import TestCase, mock

from tests_helpers.fake_file import fake_ini_file
from config.reader import read, validate_filename, MissingFilenameException


class TestConfigReader(TestCase):
    @mock.patch('config.reader.configparser.open')
    def test_read(self, mock_open):
        """
        GIVEN parameter filename is a valid string
        WHEN the read function executes
        THEN it should return a dictionary with read values
        """
        filename = 'feddit.ini'
        section_name = 'options'
        mock_open.return_value = fake_ini_file()

        config = read(filename)
        self.assertTrue(config.has_section(section_name))

    def test_read_with_empty_filename_raise_exception(self):
        with self.assertRaises(MissingFilenameException):
            """
            GIVEN parameter filename is empty
            WHEN the read function executes
            THEN it should raise an exception
            """
            filename = ''
            read(filename)

    def test_read_with_none_filename_raise_exception(self):
        with self.assertRaises(Exception):
            """
            GIVEN parameter filename is None
            WHEN the read function executes
            THEN it should raise an exception
            """
            filename = None
            read(filename)

    def test_validate_filename(self):
        filename = 'feddit.ini'
        validate_filename(filename)

    def test_validate_filename_none_raise_exception(self):
        with self.assertRaises(Exception):
            filename = None
            validate_filename(filename)

    def test_validate_filename_empty_raise_exception(self):
        with self.assertRaises(Exception):
            filename = ''
            validate_filename(filename)


