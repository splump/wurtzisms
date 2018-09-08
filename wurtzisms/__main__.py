#!/usr/bin/env python3
import requests
import random
import re
import time
import argparse
from bs4 import BeautifulSoup


# Website to fetch from
SITE = "https://billwurtz.com/"


def get_wurtzism():
    # Do two HTTP requests in one session
    session = requests.Session()
    page = session.get(SITE + "notebook.html")

    # Find all links by capital HREF - this is faster than BeautifulSoup
    links = re.findall(r'HREF=[\'"]?([^\'" >]+)', page.text)

    random_link = random.choice(links)
    random_wurtzism = session.get(SITE + random_link)
    wurtzism_soup = BeautifulSoup(random_wurtzism.text, features='html.parser')
    # Post contents are in plan text after </head> tag. We strip the first newline.
    return wurtzism_soup.text.lstrip()


def main():
    parser = argparse.ArgumentParser(description='Wisdom from Bill Wurtz')
    parser.add_argument('--instant', action='store_true', default=False, help='Print instantly')
    args = parser.parse_args()

    wurtzism = get_wurtzism()

    if args.instant:
        print(wurtzism)
    else:
        for char in wurtzism:
            print(char, end='', flush=True)
            # Randomize delay to simulate typing
            sleep_duration = random.randrange(1, 17, 1) / 100
            time.sleep(sleep_duration)
        print()


if __name__ == '__main__':
    main()
