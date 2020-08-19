import logging
import argparse
import os.path
import pandas as pd
from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

options = Options()
options.add_argument('--headless')
options.add_argument("--log-level=3")


def screenshot(pairs, args):
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.set_window_size(args.width, args.height)
    for hnid, url in pairs:
        try:
            fpath = os.path.join(args.save_dir, f'{hnid}.png')
            if os.path.isfile(fpath):
                print(f'File already exists for {hnid} {url}')
                continue
            print(f'Processing {hnid} {url}')
            driver.get(url)
            driver.save_screenshot(fpath)
            print(f'Done processing {hnid} {url}')
        except Exception as e:
            print(f'Error occurred for {hnid} {url}', e)


def chonker(pairs, n):
    for i in range(0, len(pairs), n):
        yield pairs[i:i+n]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_file', type=str,
                        required=True, help='path to url csv')
    parser.add_argument('--save_dir', type=str,
                        default='images/', help='path to save screenshots')
    parser.add_argument('--width', type=str, default=1024,
                        help='screenshot width')
    parser.add_argument('--height', type=str, default=2048,
                        help='screenshot height')
    parser.add_argument('--n_jobs', type=int, default=8,
                        help='no. of browser instances')
    parser.add_argument('--chunk_size', type=int, default=200,
                        help='no. of urls per browser instance')

    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    df = pd.read_csv(args.url_file)

    id_vs_url = {}
    for idx, row in df[['id', 'url']].iterrows():
        id_vs_url[row.id] = row.url

    # We split the urls into chunks and run `n` webdrivers in parallel
    while True:
        try:
            Parallel(n_jobs=args.n_jobs)(delayed(screenshot)(pair, args)
                                         for pair in chonker(
                                               list(id_vs_url.items()), 
                                               args.chunk_size))
        except:
            pass
