import unittest

from subtitleDownloader import sub_downloader, main

class MyTestCase(unittest.TestCase):

    def test_main(self):
        file_paths = ["E:\Projects\SideProjects\Test\SubtitleDownloader\dexter.mp4"]
        main(file_paths)


if __name__ == '__main__':
    unittest.main()
