import unittest
from os import path, remove

from subtitleDownloader import main, sub_downloader, parse_video_names


class MyTestCase(unittest.TestCase):

    def test_main(self):
        file_paths = ["E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.mp4"]
        subtitle_file = "E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.srt"
        main(file_paths)

        self.assertEquals(path.isfile(subtitle_file), True)

        remove(subtitle_file)

    def test_parse_directory(self):
        file_paths = ["E:\Projects\SideProjects\Test\SubtitleDownloader"]
        videos_names = parse_video_names(file_paths)
        self.assertEquals(videos_names, ["E:\\Projects\\SideProjects\\Test\\SubtitleDownloader\\dexter.mp4"])

    def test_parse_file(self):
        file_paths = ["E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.mp4"]
        videos_names = parse_video_names(file_paths)
        self.assertEquals(videos_names, ["E:\\Projects\\SideProjects\\Test\\SubtitleDownloader\\dexter.mp4"])

    def test_parse_file_error(self):
        file_paths = ["E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.mp3"]
        videos_names = parse_video_names(file_paths)
        self.assertEquals(videos_names, [])

if __name__ == '__main__':
    unittest.main()