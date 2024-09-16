#!/usr/bin/env python3

import requests
from pathlib import Path
from time import time as now
# from attrdict import AttrDict
from urllib.request import urlretrieve
from code.extractor import Extractor

dl_folder = Path('downloads')
media_folder = dl_folder / 'media'
pages_folder = dl_folder / 'pages'


class Downloader:
    def __init__(self):
        self.s = self.create_session()
        self.ex = Extractor(self)

    def create_session(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            "Accept-Language": "en,en-US;q=0,5",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
        }
        cookies = {
            "over18": '1',
            "age_verified": "1",
        }
        s = requests.session()
        s.headers.update(headers)
        s.cookies.update(cookies)
        return s


    def download_page(self, url, page, args):
        filename = f"{args.sub}-{args.tab}-{args.sort_by}.{page:03d}.html"
        filepath = pages_folder / filename

        print(f"\nScrapping : {url} ...")

        if not filepath.exists() or filepath.stat().st_mtime < now() - 24 * 60 * 60:
            r = self.request(url)
            with open(filepath, 'w+') as fd:
                fd.write(r.text)
        with open(filepath, 'r') as fd:
            html = fd.read()

        posts = self.ex.extract_pages(html)
        sub_media_folder = media_folder / args.sub
        sub_media_folder.mkdir(exist_ok=True, parents=True)

        for post in posts:
            media_url = self.ex.extract_media_url(post)

            if media_url:
                segments = media_url.split('?')[0].rstrip('/').split('/')
                media_name = f"{args.sub}-"
                media_name += '-'.join(segments[-2:]) if len(segments) >= 5 else segments[-1]
                if '.' not in media_name:
                    media_name += '.mp4'
                self.download_media(media_url, sub_media_folder / media_name, post)

        return posts[-1]['id']


    def request(self, url, raise_exception=True, **kwargs):
        error = None
        try:
            r = self.s.get(url, **kwargs)
        except Exception as e:
            error = str(e)
        finally:
            if error is None and r.status_code != 200:
                error = "HTTP Error {r.status_code} for {url}"
            if error is not None:
                if raise_exception:
                    raise Exception(error)
                print(error)
                return None
            return r


    def download_media(self, url, filepath, post):
        if filepath.exists(): return

        print(f"Download : {url} ...")
        try:
            urlretrieve(url, str(filepath))
        except Exception as e:
            print(f"\tDownload error for permalink : {post['permalink']} | {e!s}")
