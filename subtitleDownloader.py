#!/usr/bin/env python
# -------------------------------------------------------------------------------
# Name      : subtitle downloader
# Purpose   : One step subtitle download
#
# Authors   : manoj m j, arun shivaram p, Valentin Vetter, niroyb
# Edited by : Valentin Vetter
# Created   :
# Copyright : (c) www.manojmj.com
# Licence   : GPL v3
# -------------------------------------------------------------------------------

# TODO: use another DB if subs are not found on subDB

import hashlib
import logging
import os
import sys

PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    from urllib2 import Request, urlopen
if PY_VERSION == 3:
    from urllib.request import Request, urlopen

HTTP_API_THESUBDB = "http://api.thesubdb.com"


class FileNotVideoError(Exception):
    pass


class SubtitleFileExistError(Exception):
    pass


def get_hash(file_path):
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def write_subtitles_to_disk(file_path, response, root):
    with open(root + ".srt", "wb") as subtitle:
        subtitle.write(response)
        logging.info("Subtitle successfully downloaded for " + file_path)




def main(arguments):
    root, _ = os.path.splitext(arguments[0])
    logging.basicConfig(filename=root + '.log', level=logging.INFO)
    logging.info("Started with params " + str(sys.argv))

    video_paths = parse_video_names(arguments)
    for video_path in video_paths:
        try:
            status, response = get_subtitles_from_subdb(video_path)

            root, extension = os.path.splitext(video_path)
            # Skip this file if it is not a video_path
            if extension not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",
                                 ".3g2"]:
                raise FileNotVideoError

            if os.path.exists(root + ".srt"):
                raise SubtitleFileExistError

            write_subtitles_to_disk(video_path, response, root)
        except (FileNotVideoError, SubtitleFileExistError) as e:
            logging.error("Error: %s for file: %s", str(e), video_path)
            continue


def parse_video_names(args):
    videos_names = []

    def extract_videos(file_path, videos_names):
        _, extension = os.path.splitext(file_path)
        if extension in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",
                         ".3g2"]:
            videos_names.append(file_path)

    for path in args:
        if os.path.isdir(path):
            # Iterate the root directory recursively using os.walk and for each video file present get the subtitle
            traverse_directory(extract_videos, path, videos_names)
        else:
            extract_videos(path, videos_names)

    return videos_names


def traverse_directory(extract_videos, path, videos_names):
    for dir_path, _, file_names in os.walk(path):
        for filename in file_names:
            file_path = os.path.join(dir_path, filename)
            extract_videos(file_path, videos_names)


def get_subtitles_from_subdb(file_path):
    headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
    url = HTTP_API_THESUBDB + "/?action=download&hash=" + get_hash(file_path) + "&language=en"
    request = Request(url, "", headers)
    response = urlopen(request)
    return response.getcode(), response.read()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)

    main(sys.argv)
