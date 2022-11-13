from unittest import TestCase, mock
from unittest.mock import MagicMock


from reddit.videos import save, create, create_all


class TestRedditVideos(TestCase):
    @mock.patch('reddit.videos.get_config')
    @mock.patch('reddit.videos.download')
    @mock.patch('reddit.videos.writer')
    def test_save(self, mock_writer, mock_download, mock_get_config):
        """
        GIVEN a video file url with a new filename
        WHEN the video is downloaded
        THEN it should be saved with the given filename
        """
        mocked_request = MagicMock()
        mocked_request.content = ""
        mock_get_config.return_value = {}
        mock_download.return_value = mocked_request
        filename = "avideo.mp4"
        url = "http://www.avideo.local/avideo.mp4"
        save(url, filename)
        self.assertTrue(mock_writer.called)

    @mock.patch('reddit.videos.get_config')
    def test_save_download_error(self, mock_get_config):
        with self.assertRaises(Exception):
            """
            GIVEN a video file url with a new filename
            WHEN the video is downloaded
            THEN it should be raised an exception
            """
            mocked_request = MagicMock()
            mocked_request.status_code = "500"
            mock_get_config.return_value = {}
            filename = "avideo.mp4"
            url = "http://www.avideo.com/avideo.mp4"
            save(url, filename)

    @mock.patch('reddit.videos.get_config')
    @mock.patch('reddit.videos.writer')
    def test_save_write_file_error(self, mock_writer, mock_get_config):
        with self.assertRaises(Exception):
            """
            GIVEN a video file url with a new filename
            WHEN the video is wrote to filesystem
            THEN it should be raised an exception
            """
            mocked_request = MagicMock()
            mocked_request.content = ""
            mock_get_config.return_value = {}
            mock_writer.return_value.raiseError.side_effect = FileExistsError()
            filename = "avideo.mp4"
            url = "http://www.avideo.com/avideo.mp4"
            save(url, filename)

    @mock.patch('reddit.videos.writer')
    @mock.patch('reddit.videos.download')
    @mock.patch('reddit.videos.get_config')
    @mock.patch('reddit.videos.merge')
    def test_create_video(self, mock_merge, mock_get_config, mock_download, mock_writer):
        """
        GIVEN a video file valid url
        WHEN the video is downloaded from reddit
        THEN it should be saved
        """
        mocked_request = MagicMock()
        mocked_request.content = ""
        mock_download.return_value = mocked_request
        mocked_config = {"rootlocation": "", "targetlocation": ""}
        mock_get_config.return_value = mocked_config
        url = "https://v.redd.it/k1p5bapj17201/DASH_600_K"
        create(url)
        self.assertTrue(mock_merge.called)

    @mock.patch('reddit.videos.get_config')
    def test_create_video_raise_exception(self, mock_get_config):
        with self.assertRaises(Exception):
            """
            GIVEN a video file invalid url
            WHEN the video is downloaded from reddit
            THEN it should be raised an exception
            """
            mocked_config = {"rootlocation": "", "targetlocation": ""}
            mock_get_config.return_value = mocked_config
            url = "https://v.redd.it/"
            create(url)

    @mock.patch('reddit.videos.create')
    def test_create_all_videos(self, mock_create):
        """
        GIVEN a video file list
        WHEN the videos are downloaded from reddit
        THEN they should be saved
        """
        videos = ["https://v.redd.it/k1p5bapj17201/DASH_600_K", "https://v.redd.it/k1p5bapj17202/DASH_600_K",
                  "https://v.redd.it/k1p5bapj17203/DASH_600_K"]
        create_all(videos)
        self.assertTrue(mock_create.call_count, 3)

    @mock.patch('reddit.videos.time')
    @mock.patch('reddit.videos.create')
    def test_create_all_videos_delay_between_each_others(self, mock_create, mock_time):
        """
        GIVEN a video file list
        WHEN the videos are downloaded from reddit
        THEN there should be a delay time between one download and the others
        """
        videos = ["https://v.redd.it/k1p5bapj17201/DASH_600_K", "https://v.redd.it/k1p5bapj17202/DASH_600_K",
                  "https://v.redd.it/k1p5bapj17203/DASH_600_K"]
        create_all(videos)
        self.assertTrue(mock_time.sleep.call_count, 3)
