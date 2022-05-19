from email.header import Header
import imp
import requests
from bs4 import BeautifulSoup



class Scrapper:

    def __init__(self, url):
        self.Headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
        self.url = url

    def scrape_reviews(self):
        soup = self.html_code(self.url)
        review_data = self.fetch_customer_reviews(soup)
        review_result = self.preprocess_data(review_data)
        return review_result

    def fetch_product_data(self, url):
        html_data = requests.get(url, headers=self.Headers)
        return html_data.text

    def html_code(self, url):
        htmldata = self.fetch_product_data(url)
        soup = BeautifulSoup(htmldata)
        return (soup)

    def fetch_customer_reviews(self, soup):
        data_str = ""
        for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
            data_str = data_str + item.get_text()
        result = data_str.split("\n")
        return (result)

    def preprocess_data(self, review_data):
        review_result = []
        for i in review_data:
            if i == "":
                pass
            else:
                review_result.append(i)
        return review_result
