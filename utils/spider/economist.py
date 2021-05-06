import requests
from bs4 import BeautifulSoup as Soup, Tag
from smartify import Attribute

from utils.spider.base_spider import BaseSpider


class EconomistContent:
    def __init__(self, url, category, sub_headline, headline, description, image, body):
        self.category = category
        self.sub_headline = sub_headline
        self.headline = headline
        self.description = description
        self.image = image
        self.url = url

        self.body = []
        self.section = []
        for paragraph in body:  # type: Tag
            self.section.append(len(paragraph.contents) == 1 and paragraph.contents[0].name == 'strong')
            self.body.append(paragraph.text)

    def d(self):
        return dict(
            category=self.category,
            sub_headline=self.sub_headline,
            headline=self.headline,
            description=self.description,
            image=self.image,
            url=self.url,
        )


class EconomistSpider(BaseSpider):
    URL = 'https://www.economist.com'

    def grab_today_url(self):
        with requests.get(self.URL) as r:
            html = r.content
        soup = Soup(html, 'html.parser')
        return soup.find(class_='headline-link').attrs['href']

    def grab(self, url: str):
        if url.startswith('/'):
            url = self.URL + url
        with requests.get(url) as r:
            html = r.content
        soup = Soup(html, 'html.parser')

        category = soup.find(class_='article__section-headline').find('a').text
        sub_headline = soup.find(class_='article__subheadline').text
        headline = soup.find(class_='article__headline').text
        description = soup.find(class_='article__description').text
        image = soup.find(class_='article__lead-image').find('meta').attrs['content']

        body = soup.find_all(class_='article__body-text')
        return EconomistContent(
            category=category,
            sub_headline=sub_headline,
            headline=headline,
            description=description,
            image=image,
            body=body,
            url=url,
        )

    def grab_today_news(self):
        news_url = self.grab_today_url()
        print(news_url)
        return self.grab(news_url)
