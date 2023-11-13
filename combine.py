import ffmpeg
import logging

def combine(input_video_path, input_audio_path, output_path):
    input_video = ffmpeg.input(input_video_path)
    input_audio = ffmpeg.input(input_audio_path)

    logging.info('Concatenating %s and %s' % (input_video_path, input_audio_path))
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_path, loglevel="quiet").run_async()

if __name__ == '__main__':
    combine()
