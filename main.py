import os
import sys
from download import download
from combine import combine

def main():
    # config file
    config_file = 'config'
    # check if config file exists
    with open(config_file, 'r') as f:
        lines = f.read().strip().split('\n')
    
    for link in lines:
        file_name = download(link)
        combine(file_name + '_video.mp4', file_name + '_audio.mp4', file_name + '.mp4')

    


if __name__ == '__main__':
    main()
