from unittest import TestCase, mock
from unittest.mock import MagicMock, mock_open, patch

from filesystem.file import writer


class TestFilesystemFile(TestCase):
    @mock.patch("filesystem.file.open")
    def test_file_is_opened(self, mock_open):
        """
        GIVEN a content, a filename and a mode
        WHEN is trying to open the file
        THEN it should be opening
        """
        mock_open.return_value = MagicMock()
        content = ""
        filename = "file.txt"
        mode = "w"
        writer(content, filename, mode)
        self.assertTrue(mock_open.called)

    @mock.patch("filesystem.file.open")
    def test_file_opening_raised_exception(self, mock_open):
        with self.assertRaises(Exception):
            """
            GIVEN a content, a filename and a mode
            WHEN is trying to open the file
            THEN an exception should be raised
            """
            mock_open.side_effect = OSError()
            content = ""
            filename = "file.txt"
            mode = "w"
            writer(content, filename, mode)

    def test_file_is_writen(self):
        with patch("filesystem.file.open", mock_open()) as mocked_file:
            """
            GIVEN a content, a filename and a mode
            WHEN is trying to write the content to a file
            THEN it should be opening
            """
            content = ""
            filename = "file.txt"
            mode = "w"

            writer(content, filename, mode)
            self.assertTrue(mocked_file().write.called)

    @mock.patch("filesystem.file.open")
    def test_file_wrote_raised_exception(self, mocked_file):
        with self.assertRaises(Exception), patch("filesystem.file.open", mock_open()) as mocked_file:
            """
            GIVEN a content, a filename and a mode
            WHEN is trying to write the content to a file
            THEN an exception should be raised
            """
            mocked_file().write.side_effect = FileNotFoundError()
            content = ""
            filename = "file.txt"
            mode = "w"
            writer(content, filename, mode)

