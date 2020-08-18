import logging
import pandas as pd
from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

options = Options()
options.add_argument('--headless')
options.add_argument("--log-level=3")

df = pd.read_csv('hn_urls.csv')

id_vs_url = {}
for idx, row in df[['id', 'url']].iterrows():
    id_vs_url[row.id] = row.url


def screenshot(pairs):
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.set_window_size(1024, 2048)
    for hnid, url in pairs:
        print(f'Processing {hnid} {url}')
        driver.get(url)
        driver.save_screenshot(f'data/images/{hnid}.png')
        print(f'Done processing {hnid} {url}')


def chonker(pairs, n):
    for i in range(0, len(pairs), n):
        yield pairs[i: i+n]


# We split the urls into chunks and run `n` webdrivers in parallel
Parallel(n_jobs=8)(delayed(screenshot)(pair)
                   for pair in chonker(list(id_vs_url.items()), 100))
