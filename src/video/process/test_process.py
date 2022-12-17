from unittest import TestCase, mock
from unittest.mock import MagicMock

from tests_helpers.fake_file import fake_ini_file
from video.process import merge


class TestProcess(TestCase):
    @mock.patch('video.process.get_config')
    @mock.patch('os.system')
    def test_merge(self, mock_os_system, mock_config):
        ffmpeg_location = 'ffmpeglocation=C://this-is-a-test'
        mock_config = MagicMock()
        mock_config.return_value = fake_ini_file(ffmpeg_location)
        mock_os_system.return_value = MagicMock()
        audio = "C://audio-route"
        video = "C://video-route"
        filename = "video.mp4"
        merge(audio, video, filename)
        self.assertTrue(mock_os_system.called)
