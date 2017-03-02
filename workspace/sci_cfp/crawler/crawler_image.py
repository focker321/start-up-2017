__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import ImageEvent

from bs4 import BeautifulSoup
import re
import urllib2
from crawler import Crawler


class CrawlerImage(Crawler):
    def __init__(self):
        self.base_url = "http://www.worldcityphotos.org/"
        self.events_url = self.base_url + ""
        self.search = self.base_url + "/cfp/servlet/tool.search"
        self.max_number_pages = 20

    def crawler_page(self, number_page):
        events_url = self.events_url
        try:
            page = urllib2.urlopen(events_url)
            soup = BeautifulSoup(page, "lxml")
            # /html/body/div/table[2]/tbody/tr/td[2]/div[1]/table/tbody/tr
            tr = soup.findAll("table")[1].find("table").find("tr")
            event_urls = tr.findAll('a')
            for idx, event_url in enumerate(event_urls[138:]):
                url = self.get_prop_span(event_url, "href")
                country_name = self.get_prop_span(event_url, "text")
                self.crawler_element(url, country_name)
        except urllib2.HTTPError:
            pass

    def crawler_element(self, event_url, country_name):
        try:
            page = urllib2.urlopen(self.base_url + event_url.replace("./", ""))
            soup = BeautifulSoup(page, "lxml")
            event_urls = soup.findAll('a')
            cities = []
            for event_url in event_urls:
                url_city = self.base_url + self.get_prop_span(event_url, "href")
                url_name = self.get_prop_span(event_url, "clean_text")
                url_name = url_name.split()
                if len(url_name) >= 3:
                    city_name = url_name[1]
                else:
                    city_name = url_name[0]
                if city_name in cities or city_name == "Directory" or city_name == "jpg" or city_name == "Parent" or not re.match("^[A-Za-z]*$", city_name):
                    continue
                print(city_name, country_name, url_city)
                image_event = ImageEvent()
                image_event.id = country_name + city_name
                image_event.city_name = city_name
                image_event.country_name = country_name
                image_event.url_image = url_city
                image_event.save()
                cities.append(city_name)
        except urllib2.HTTPError:
            pass




if __name__ == '__main__':
    crawler_image = CrawlerImage()
    crawler_image.crawler()