#!/usr/bin/env python3
import requests
import random
import re
import time
import argparse
from bs4 import BeautifulSoup

# Add option to type it out slowly
parser = argparse.ArgumentParser(description='Wisdom from Bill Wurtz')
parser.add_argument('--type', action='store_true', default=False, help='Type it out slowly')
args = parser.parse_args()

# Website to fetch from
SITE = "https://billwurtz.com/"

# Do two HTTP requests in one session
session = requests.Session()
page = session.get(SITE + "notebook.html")

# Find all links by capital HREF - this is faster than BeautifulSoup
links = re.findall(r'HREF=[\'"]?([^\'" >]+)', page.text)

random_link = random.choice(links)
random_wurtzism = session.get(SITE + random_link)
wurtzism_soup = BeautifulSoup(random_wurtzism.text, features='html.parser')
# Post contents are in plan text after </head> tag. We strip the first newline.
wurtzism = wurtzism_soup.text.lstrip()

if args.type:
    for char in wurtzism:
        print(char, end='', flush=True)
        # Randomize delay to simulate typing
        sleep_duration = random.randrange(1, 17, 1) / 100
        time.sleep(sleep_duration)
    print()
else:
    print(wurtzism)
