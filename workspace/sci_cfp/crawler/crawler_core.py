__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event, Qualification
from crawler_event import CrawlerEvent
from crawler import Crawler
from bs4 import BeautifulSoup
import re
import urllib2
import datetime


class CrawlerCore(Crawler):
    def __init__(self):
        self.base_url = "http://portal.core.edu.au"
        self.events_url = self.base_url + "/conf-ranks/"
        self.max_number_pages = 44
        self.crawler_event = CrawlerEvent()

    def crawler_page(self, number_page):
        events_url = self.events_url + "?search=&by=all&source=all&sort=atitle&page=" + str(number_page)
        page = urllib2.urlopen(events_url)
        soup = BeautifulSoup(page, "lxml")
        events_info = soup.find_all("tr", onclick=re.compile("/conf-ranks"))
        for event_info in events_info:
            qualification = self.crawler_element(event_info)
            event = self.crawler_event.retrieve_event(qualification.acronym, qualification.title)
            qualification.event_id = event.id
            qualification.save()

    def crawler_element(self, event_info):
        qualification = None
        columns = event_info.find_all("td")
        if len(columns) == 8:
            title = self.get_prop_span(columns[0], "clean_text")
            acronym = self.get_prop_span(columns[1], "clean_text")
            source = self.get_prop_span(columns[2], "clean_text")
            rank = self.get_prop_span(columns[3], "clean_text")
            print(title, acronym, source, rank)
            qualification = Qualification()
            qualification.acronym = acronym
            qualification.title = title
            qualification.source = source
            qualification.rank = rank
        return qualification

    def crawler_search(self, acronym):
        qualification = None
        qualis_url = self.events_url + "?search=" + acronym + "&by=acronym&source=all&sort=atitle&page=1"
        page = urllib2.urlopen(qualis_url)
        soup = BeautifulSoup(page, "lxml")
        events_info = soup.find_all("tr", onclick=re.compile("/conf-ranks"))
        for event_info in events_info:
            qualification = self.crawler_element(event_info)
            if qualification.acronym == acronym:
                break
        return qualification

if __name__ == '__main__':
    crawler_core = CrawlerCore()
    crawler_core.crawler()
