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
import shutil
import sys
import zipfile
from time import sleep
from bs4 import BeautifulSoup
from requests import get

HTTP_API_THESUBDB = "http://api.thesubdb.com"

PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    from urllib2 import Request, urlopen
if PY_VERSION == 3:
    from urllib.request import Request, urlopen


def get_hash(file_path):
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


class FileNotVideoError(Exception):
    pass


class SubtitleFileExistError(Exception):
    pass


def sub_downloader(file_path):
    root, extension = os.path.splitext(file_path)
    # Skip this file if it is not a video
    if extension not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",
                         ".3g2"]:
        raise FileNotVideoError

    if os.path.exists(root + ".srt"):
        raise SubtitleFileExistError

    response_code, response = get_subtitles_from_subdb(file_path)
    write_subtitles_to_disk(file_path, response, root)
    
    return response_code


def write_subtitles_to_disk(file_path, response, root):
    with open(root + ".srt", "wb") as subtitle:
        subtitle.write(response)
        logging.info("Subtitle successfully downloaded for " + file_path)


def get_subtitles_from_subdb(file_path):
    headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
    url = HTTP_API_THESUBDB + "/?action=download&hash=" + get_hash(file_path) + "&language=en"
    request = Request(url, "", headers)
    response_code = urlopen(request).getcode()
    response = urlopen(request).read()
    return response_code, response


def sub_downloader2(file_path):
    try:
        root, extension = os.path.splitext(file_path)
        if extension not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",
                             ".3g2"]:
            return
        if os.path.exists(root + ".srt"):
            return
        j = -1
        root2 = root
        for idx, char in enumerate(reversed(root)):
            if char == "\\" or char == "/":
                j = len(root) - 1 - idx
                break
        root = root2[j + 1:]
        root2 = root2[:j + 1]
        r = get("http://subscene.com/subtitles/release?q=" + root);
        soup = BeautifulSoup(r.content, "lxml")
        atags = soup.find_all("a")
        href = ""
        for i in range(0, len(atags)):
            spans = atags[i].find_all("span")
            if len(spans) == 2 and spans[0].get_text().strip() == "English":
                href = atags[i].get("href").strip()
        if len(href) > 0:
            r = get("http://subscene.com" + href);
            soup = BeautifulSoup(r.content, "lxml")
            lin = soup.find_all('a', attrs={'id': 'downloadButton'})[0].get("href")
            r = get("http://subscene.com" + lin);
            subtitle_file = open(root2 + ".zip", 'wb')
            for chunk in r.iter_content(100000):
                subtitle_file.write(chunk)
                subtitle_file.close()
                sleep(1)
                zip = zipfile.ZipFile(root2 + ".zip")
                zip.extractall(root2)
                zip.close()
                os.unlink(root2 + ".zip")
                shutil.move(root2 + zip.namelist()[0], os.path.join(root2, root + ".srt"))
    except:
        # Ignore exception and continue
        print("Error in fetching subtitle for " + file_path)
        print("Error", sys.exc_info())
        logging.error("Error in fetching subtitle for " + file_path + str(sys.exc_info()))


def main(arguments):
    root, _ = os.path.splitext(arguments[0])
    logging.basicConfig(filename=root + '.log', level=logging.INFO)
    logging.info("Started with params " + str(sys.argv))

    videos_names = parse_video_names(arguments)
    for video in videos_names:
        try:
            status = sub_downloader(video)
        except (FileNotVideoError, SubtitleFileExistError) as e:
            logging.error("Error: %s for file: %s", str(e), video)
            continue

        if status != 200:
            # download subs from subscene if not found in subdb
            sub_downloader2(video)


def parse_video_names(args):
    videos_names = []
    for path in args:
        if os.path.isdir(path):
            # Iterate the root directory recursively using os.walk and for each video file present get the subtitle
            for dir_path, _, file_names in os.walk(path):
                for filename in file_names:
                    file_path = os.path.join(dir_path, filename)
                    extract_videos(file_path, videos_names)
        else:
            extract_videos(path, videos_names)

    return videos_names


def extract_videos(file_path, videos_names):
    _, extension = os.path.splitext(file_path)
    if extension in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp", ".3g2"]:
        videos_names.append(file_path)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)

    main(sys.argv)
