import pytube

def download(url):
    yt = pytube.YouTube(url, proxies={'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'})
    file_name = yt.title
    thumbnail_url = yt.thumbnail_url
    print(thumbnail_url)
    print(yt.streams)

    # Get highest bitrate audio stream for given codec (defaults to mp4)
    # ref: https://pytube.io/en/latest/_modules/pytube/query.html#StreamQuery.get_audio_only
    audio = yt.streams.get_audio_only(subtype='mp4')
    print(audio)
    # download
    audio.download(filename=f'{file_name}_audio.mp4')

    # Get the highest resolution video, without audio
    video = yt.streams.filter(only_video=True, subtype='mp4').order_by('resolution').desc().first()
    print(video)
    # download
    video.download(filename=f'{file_name}_video.mp4')
    return file_name

if __name__ == '__main__':
    download()
