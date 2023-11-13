import pytube

def main():
    url = 'https://www.youtube.com/watch?v=Ed4WOs29E08'
    yt = pytube.YouTube(url)
    title = yt.title
    print(title)
    thumbnail_url = yt.thumbnail_url
    print(thumbnail_url)
    print(yt.streams)

    # Get highest bitrate audio stream for given codec (defaults to mp4)
    # ref: https://pytube.io/en/latest/_modules/pytube/query.html#StreamQuery.get_audio_only
    audio = yt.streams.get_audio_only(subtype='mp4')
    print(audio)

    # Get the highest resolution video, without audio
    videos = yt.streams.filter(only_video=True, subtype='mp4').order_by('resolution').desc()
    print(videos)

if __name__ == '__main__':
    main()
