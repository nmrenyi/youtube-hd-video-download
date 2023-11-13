import os
import argparse
import multiprocessing

import pytube
from download import download
from combine import combine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', '-w', type=int, default=0, help='number of download workers, default 0 (single process)')
    parser.add_argument('--config', '-c', type=str, default='config.example', help='config file, default config.example')
    parser.add_argument('--link', '-l', type=str, default=None, help='single link to download, default None')
    return parser.parse_args()

def process(link):
    intermidiate_dir = 'intermidiate-videos'
    final_dir = 'final-videos'
    if not os.path.exists(intermidiate_dir):
        os.makedirs(intermidiate_dir)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    try:
        file_name = download(link, intermidiate_dir)
    except pytube.exceptions.AgeRestrictedError:
        print('Age restricted video, skipping')
        return
    except Exception as e:
        print('Error occured, skipping')
        print(e)
        return
    combine(os.path.join(intermidiate_dir, file_name + '_video.mp4'), os.path.join(intermidiate_dir, file_name + '_audio.mp4'), os.path.join(final_dir, file_name + '.mp4'))


def main():
    args = parse_args()

    if args.link:
        process(args.link)
    else:
        with open(args.config, 'r') as f:
            lines = f.read().strip().split('\n')
        
        if args.worker > 0:
            pool = multiprocessing.Pool(args.worker)
            pool.map(process, lines)

        else:
            for link in lines:
                process(link)



if __name__ == '__main__':
    main()
