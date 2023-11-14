import os
import unicodedata
import re
import logging
import pytube
import requests

def slugify(value, allow_unicode=False):
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

def download(url, intermidiate_dir):
    yt = pytube.YouTube(url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
    file_name = slugify(yt.title)
    thumbnail_url = yt.thumbnail_url
    logging.info(file_name)
    logging.info(thumbnail_url)

    # Get highest bitrate audio stream for given codec (defaults to mp4)
    # ref: https://pytube.io/en/latest/_modules/pytube/query.html#StreamQuery.get_audio_only
    audio = yt.streams.get_audio_only(subtype='mp4')
    # download
    logging.info('Downloading %s' % audio)
    audio.download(filename=os.path.join(intermidiate_dir, f'{file_name}_audio.mp4'))

    # Get the highest resolution video, without audio
    video = yt.streams.filter(only_video=True, subtype='mp4').order_by('resolution').desc().first()
    # download
    logging.info('Downloading %s' % video)
    video.download(filename=os.path.join(intermidiate_dir, f'{file_name}_video.mp4'))
    return file_name

def get_pic(url):
    r = requests.get(url, stream=True, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
    with open('./test.jpg', mode='wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    get_pic('https://i.ytimg.com/vi/J0w0t4Qn6LY/hq720.jpg?sqp=-oaymwEXCNUGEOADIAQqCwjVARCqCBh4INgESFo&rs=AOn4CLCSnM7iOtKzkFaBpHlPvKfgrr_umg')
