import pytube

def main():
    url = 'https://www.youtube.com/watch?v=Ed4WOs29E08'
    yt = pytube.YouTube(url)
    title = yt.title
    print(title)
    thumbnail_url = yt.thumbnail_url
    print(thumbnail_url)
    print(yt.streams)



if __name__ == '__main__':
    main()
