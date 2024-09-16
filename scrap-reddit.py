#!/usr/bin/env python3

import sys
import argparse
from code.scrap import scrap


def parse_args():
    parser = argparse.ArgumentParser(description="Reddit image scrapper")
    parser.add_argument('sub', type=str, help="The name of the subreddit to scrap")
    parser.add_argument('--user', '-u', action="store_true", help="Scrap user page instead of subreddit")
    parser.add_argument('--tab', '-t', type=str, default="submitted", help="Tab to scrap in user page (default=submitted): overview, comments, submitted")
    parser.add_argument('--sort_by', '-s', type=str, default="hot", help="Sorting of the subreddit (default=hot): hot, new, rising, controversial, top")
    parser.add_argument('--limit', '-l', type=int, default=sys.maxsize, help="Limit of pages to download (default: unlimited)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    scrap(args)
