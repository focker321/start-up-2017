__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event, Qualification
from crawler_event import CrawlerEvent
from crawler_core import CrawlerCore
from crawler import Crawler
from bs4 import BeautifulSoup
import re
import urllib2
import time
from selenium import webdriver


class CrawlerQualis(Crawler):
    def __init__(self):
        self.base_url = "http://qualis.ic.ufmt.br/"
        self.events_url = ""
        self.max_number_pages = 1
        self.crawler_event = CrawlerEvent()
        self.crawler_core = CrawlerCore()

    def crawler_page(self, number_page):
        events_url = self.base_url
        # page = urllib2.urlopen(events_url)
        page = self.selenium_browser(events_url)
        soup = BeautifulSoup(page, "lxml")
        table = soup.find("table", id=re.compile("tb-conferencias"))
        tbody = table.find("tbody")
        events_info = tbody.find_all("tr")
        for event_info in events_info:
            columns = event_info.find_all("td")
            if len(columns) == 4:
                acronym = self.get_prop_span(columns[0], "clean_text")
                title = self.get_prop_span(columns[1], "clean_text")
                source = "QUALIS-IC-UFMT-BR"
                rank = self.get_prop_span(columns[3], "clean_text")
                print(title, acronym, source, rank)
                qualification_core = self.crawler_core.crawler_search(acronym)
                event = self.crawler_event.retrieve_event(acronym, title)
                if qualification_core is not None:
                    qualification_core.event_id = event.id
                    qualification_core.save()

                qualification = Qualification()
                qualification.source = source
                qualification.rank = rank
                qualification.event_id = event.id
                qualification.title = title
                qualification.acronym = acronym
                qualification.save()

    def selenium_browser(self, url):
        browser = webdriver.PhantomJS()
        browser.get(url)
        page = browser.page_source
        browser.quit()
        return page

if __name__ == '__main__':
    crawler_qualis = CrawlerQualis()
    crawler_qualis.crawler()