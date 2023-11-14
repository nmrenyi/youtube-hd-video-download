import os
import unicodedata
import re
import logging
import pytube
import requests

from pytube import YouTube
from tqdm import tqdm

class VideoDownloader:
    def __init__(self, url, output_path='downloads'):
        self.url = url
        self.output_path = output_path
        self.video_total_size = 0
        self.video_pbar = None
        self.audio_pbar = None

        yt = pytube.YouTube(self.url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
        self.file_name = self.slugify(yt.title)
        logging.info('Downloading %s from %s into %s' % (self.file_name, url, output_path))

    def video_progress_callback(self, chunk, file_handle, bytes_remaining):
        # Update the progress bar with the number of bytes downloaded
        self.video_pbar.update(self.video_total_size - bytes_remaining)

    def audio_progress_callback(self, chunk, file_handle, bytes_remaining):
        # Update the progress bar with the number of bytes downloaded
        self.audio_pbar.update(self.audio_total_size - bytes_remaining)


    def download_pic(self):
        yt = pytube.YouTube(self.url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
        thumbnail_url = yt.thumbnail_url
        file_name = self.slugify(yt.title)
        self.get_pic(thumbnail_url, os.path.join(self.output_path, f'{file_name}.jpg'))


    def download_video(self):
        yt = pytube.YouTube(self.url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}, on_progress_callback=self.video_progress_callback)
        file_name = self.slugify(yt.title)

        # Get the highest resolution video, without audio
        video = yt.streams.filter(only_video=True, subtype='mp4').order_by('resolution').desc().first()
        # Set up the progress bar
        self.video_total_size = video.filesize
        self.video_pbar = tqdm(total=self.video_total_size, unit='B', unit_scale=True)

        # download
        logging.info('Downloading %s' % video)
        video.download(filename=f'{file_name}_video.mp4', output_path=self.output_path)
        self.video_pbar.close()
        return file_name

    def download_audio(self):
        yt = pytube.YouTube(self.url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}, on_progress_callback=self.audio_progress_callback)
        file_name = self.slugify(yt.title)

        # Get highest bitrate audio stream for given codec (defaults to mp4)
        # ref: https://pytube.io/en/latest/_modules/pytube/query.html#StreamQuery.get_audio_only
        audio = yt.streams.get_audio_only(subtype='mp4')
        # Set up the progress bar
        self.audio_total_size = audio.filesize
        self.audio_pbar = tqdm(total=self.audio_total_size, unit='B', unit_scale=True)

        # download
        logging.info('Downloading %s' % audio)
        audio.download(filename=f'{file_name}_audio.mp4', output_path=self.output_path)
        self.audio_pbar.close()
        return file_name




    def slugify(self, value, allow_unicode=False):
        """
        ref: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')


    def get_pic(self, url, path):
        r = requests.get(url, stream=True, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
        with open(path, mode='wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    get_pic('https://i.ytimg.com/vi/J0w0t4Qn6LY/hq720.jpg?sqp=-oaymwEXCNUGEOADIAQqCwjVARCqCBh4INgESFo&rs=AOn4CLCSnM7iOtKzkFaBpHlPvKfgrr_umg', './hahn.jpg')
