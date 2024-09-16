#!/usr/bin/env python3

import requests
from time import time
from pathlib import Path
from warnings import warn
from bs4 import BeautifulSoup as bs4
from code.downloader import Downloader
from code.extractor import Extractor

base_url = "https://old.reddit.com"

user_tabs = ['overview', 'comments', 'submitted', 'gilded']
user_sorts = ['top', 'hot', 'controversial', 'new']
sub_sorts = [*user_sorts, 'rising', 'gilded']


def add_user_options(url, args):
    if args.tab not in user_tabs:
        warn(f"'${args.tab}' is not a valid tab for a user page")
    if args.sort_by not in user_sorts:
        warn(f"'${args.sort_by} is not a valid sorting for a user page")
    url += f"/{args.tab}"
    url += f"?sort={args.sort}"
    return url


def add_sub_options(url, args):
    if args.sort_by not in sub_sorts:
        warn(f"'{args.sort_by} is not a valid sorting for a subreddit")
    url += f"/{args.sort_by}"
    return url


def construct_url(args):
    url = base_url
    url += '/user/' if args.user else '/r/'
    url += args.sub
    if args.user:
        url = add_user_options(url, args)
    else:
        url = add_sub_options(url, args)
    return url


def scrap_page(dl, url, page, args):

    last_id = dl.download_page(url, page, args)

    return last_id


def scrap(args):
    base_url = construct_url(args)
    dl = Downloader()
    after = None
    count = 0
    page = 1
    still_more = True
    limit = args.limit

    print(args)
    
    while still_more and count < limit:
        if after is not None:
            url = f"{base_url}?count={count}&after=t3_{after}"
            count = count + 25 if count + 25 < limit else limit
            page += 1
        else:
            url = base_url
            count = 25 if limit > 25 else limit
        try:
            print(url)
            after = scrap_page(dl, url, page, args)
            print(after)

        except Exception as e:
            print("Exception : "+ str(e))
            still_more = False

    # scrap_page(url, args)
    # https: // www.reddit.com/r/JennaLynnMeowri /?count = 25 & after = t3_gkl1li
    # https: // www.reddit.com/r/JennaLynnMeowri/new /?app = res & count = 50 & after = t3_fxw195
