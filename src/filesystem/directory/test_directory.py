from unittest import TestCase, mock

from filesystem.directory import files, clean


class TestDirectory(TestCase):
    @mock.patch("os.listdir")
    def test_lists(self, mocked_listdir):
        """
        GIVEN a directory route
        WHEN is trying to list inner files
        THEN a list with file names should be returned
        """
        mocked_listdir.return_value = [
            'file1.jpg', 'file2.txt', 'file3.mp4', 'file4.mp3'
        ]
        route = "C://prueba"
        file_list = files(route)
        self.assertTrue(len(file_list) > 0)

    @mock.patch("os.listdir")
    def test_lists_raise_exception(self, mocked_listdir):
        with self.assertRaises(Exception):
            """
            GIVEN a directory route
            WHEN is trying to list inner files
            THEN an exception should be raised
            """
            mocked_listdir.side_effect = FileNotFoundError()
            route = "C://prueba"
            files(route)

    @mock.patch("os.remove")
    @mock.patch("os.listdir")
    def test_clean(self, mocked_listdir, mocked_delete):
        """
        GIVEN a directory route
        WHEN is trying to clean it
        THEN all the files inside the directory should be deleted
        """
        mocked_listdir.return_value = [
            'file1.jpg', 'file2.txt', 'file3.mp4', 'file4.mp3'
        ]
        route = "C://prueba"
        clean(route)
        self.assertTrue(mocked_delete.called)
