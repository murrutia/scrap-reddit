#!/usr/bin/env python3
import re
from json import loads as json_loads
from bs4 import BeautifulSoup as bs4

class Extractor:

    def __init__(self, downloader):
        self.dl = downloader
        # self.base_url = base_url


    def extract_pages(self, html_str):
        posts = []
        html = bs4(html_str, 'lxml')
        things = html.select('.thing')

        for t in things:
            segments = t.attrs['data-permalink'].rstrip('/').split('/')
            t_id = segments[-2]
            t_name = segments[-1]
            posts.append({
                "url": t.attrs['data-url'],
                "id": segments[-2],
                "name": segments[-1],
                "permalink": "https://reddit.com" + t.attrs['data-permalink'],
                **t.attrs
            })
        return posts


    def extract_media_url(self, post):
        url = post['url']

        print(f"\nPost URL : {url}")

        direct_pic_sites = [
            "https://i.redd.it/",
            "https://i.imgur.com/",
            "https://imgur.com/",
        ]
        direct = False

        for site in direct_pic_sites:
            if url.startswith(site):
                direct = True
                break
        if direct:
            return url

        return self.retrieve_from_other_site(post)


    def retrieve_from_other_site(self, post):
        url = post['url']

        if url.startswith("https://gfycat.com/") or url.startswith("https://redgifs.com/"):
            try:
                r = self.dl.request(url)
            except Exception as e:
                print(f"Download error : {e!s}")
                return None

            html = bs4(r.text, 'lxml')
            # mp4 = html.find()
            return html.select('source[type="video/mp4"]')[0].attrs['src']
            # return html.select('.video source')[0].attrs['src']

        if url.startswith('https://v.redd.it/'):
            url = f"{post['permalink']}.json"
            r = self.dl.request(url)
            json = r.json()
            print(f"v.redd.it : {json[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url']}")
            return json[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url'].split('?')[0]

        if url.startswith('https://www.youporn.com/'):
            r = self.dl.request(url)
            json_str = re.search(r'video.mediaDefinition = (\[.*\])', r.text).group(1)

            json_dict = json_loads(json_str)
            nb_versions = len(json_dict)
            return json_dict[nb_versions - 1 if nb_versions < 3 else 2]['videoUrl']
            # with open('/tmp/youporn.html', 'w+') as fd:
            #     fd.write(r.text)
            # print(html.select('#videoContainer video source'))
            # return html.select('#videoContainer video source')[0].attrs['src']

        print(f"No download : {url}")

        return None
