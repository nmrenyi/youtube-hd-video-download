from multiprocessing import Pool

from download import download
from combine import combine

def work(link):
    file_name = download(link)
    combine(file_name + '_video.mp4', file_name + '_audio.mp4', file_name + '.mp4')

def main():
    # config file
    config_file = 'config'
    # check if config file exists
    with open(config_file, 'r') as f:
        lines = f.read().strip().split('\n')
    
    with Pool(10) as p:
        p.map(download, lines)



if __name__ == '__main__':
    main()
