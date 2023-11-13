import ffmpeg

def main():
    input_video = ffmpeg.input('video.mp4')
    input_audio = ffmpeg.input('audio.mp4')
    output_name = 'output.mp4'

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_name).run()

if __name__ == '__main__':
    main()
