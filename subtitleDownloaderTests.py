import unittest
from os import path, remove

from subtitleDownloader import main, parse_video_names, get_subtitles_from_subdb


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

    def test_get_subtitles_from_subdb(self):
        code, response = get_subtitles_from_subdb("E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.mp4")
        self.assertEquals(code, 200)
        self.assertEquals(response, "1\n00:00:05,000 --> 00:00:15,000\nAtention: This is a test subtitle.\n \n2 \n00:00:25,000 --> 00:00:40,000\nSubDB - the free subtitle database\nhttp://thesubdb.com\n")


if __name__ == '__main__':
    unittest.main()