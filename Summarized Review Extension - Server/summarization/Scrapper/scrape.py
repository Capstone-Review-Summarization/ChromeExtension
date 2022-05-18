from selectorlib import Extractor
import requests
import json
from time import sleep
from dateutil import parser as dateparser


class Scrape:
    def __init__(self, url):
        self.url = url
        self.e = Extractor.from_yaml_file('selectors.yml')

    def scrape(self):
        data = self.get_text(self.url)
        reviews = []
        data['next_page'] = data['all_reviews_link']
        if data:
            while data['next_page'] and len(reviews) < 50:
                data = self.get_text(
                    'https://www.amazon.in/' + data['next_page'])
                for review in data['reviews']:
                    reviews.append(review)
        return reviews

    def get_text(self, url):
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        r = requests.get(url, headers=headers)
        if r.status_code > 500:
            return None
        return self.e.extract(r.text)
