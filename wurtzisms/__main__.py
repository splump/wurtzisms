#!/usr/bin/env python3
import requests
import random
import re
import time
import argparse
import sqlite3
import os
from bs4 import BeautifulSoup


# Website to fetch from
SITE = "https://billwurtz.com/"
CACHE_PATH = "~/.cache"
CACHE_NAME = "wurtzisms.db"
REFRESH_LIMIT = 100


def debug(msg):
    if args.debug:
        print(msg)


def init_cache(path, dbname):
    path = os.path.expanduser(path)

    # Create cache path if it does not exist
    if not os.path.exists(path):
        try:
            debug("Cache path %s does not exist, creating..." % CACHE_PATH)
            os.makedirs(path)
        except:
            exit()

    # Open database and initialize tables if database is empty
    db = sqlite3.connect('%s' % (os.path.join(path, dbname)))
    c = db.cursor()
    c.execute("create table if not exists notes(link TEXT PRIMARY KEY, note TEXT);")
    c.execute("create table if not exists meta(counter INT PRIMARY KEY);")
    db.commit()
    check_cache(db)

    return db


def check_cache(db):
    c = db.cursor()
    counter = c.execute("SELECT counter FROM meta LIMIT 1;").fetchone()

    # This is most likely an empty cache, trigger automatic refresh
    if counter is None:
        debug("inserting counter at %s" % REFRESH_LIMIT)
        c.execute("INSERT INTO meta(counter) VALUES(?);", (REFRESH_LIMIT,))
        db.commit()
        counter = c.execute("SELECT counter FROM meta LIMIT 1;").fetchone()
        # refresh_cache(db)

    debug("Refresh counter is at %s (limit %s)" % (counter[0], REFRESH_LIMIT))
    if counter[0] >= REFRESH_LIMIT:
        debug("Performing refresh of cache...")
        refresh_cache(db)
        c.execute("UPDATE meta SET counter = ? WHERE counter = ?", (0, counter[0]))
    else:
        c.execute("UPDATE meta SET counter = ? WHERE counter = ?", (counter[0] + 1, counter[0]))
    db.commit()


def refresh_cache(db):
    c = db.cursor()
    num_notes = c.execute("SELECT count(*) FROM notes;").fetchone()[0]
    debug("Amount of notes in database: %s" % num_notes)

    session = requests.Session()
    page = session.get(SITE + "notebook.html")
    # Find all links by capital HREF - this is faster than BeautifulSoup
    links = re.findall(r'HREF=[\'"]?([^\'" >]+)', page.text)
    debug("Amount of notes on remote site: %s" % len(links))

    if len(links) > num_notes:
        # Insert all links that do not exist in notes
        notes = c.execute("SELECT link FROM notes;").fetchall()
        notes = [n[0] for n in notes]
        for link in links:
            if link not in notes:
                note_url = session.get(SITE + link)
                note_soup = BeautifulSoup(note_url.text, features='html.parser')
                c.execute("INSERT INTO notes(link, note) VALUES(?, ?)", (link, note_soup.text.lstrip()))
        db.commit()


def get_wurtzism():
    db = init_cache(CACHE_PATH, CACHE_NAME)
    c = db.cursor()

    random_note = c.execute("SELECT * FROM notes ORDER BY random() LIMIT 1").fetchone()[1]
    return random_note


def main():
    parser = argparse.ArgumentParser(description='Wisdom from Bill Wurtz')
    parser.add_argument('--instant', action='store_true', default=False, help='Print instantly')
    parser.add_argument('--debug', action='store_true', default=False, help='Output debug information')
    global args
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
