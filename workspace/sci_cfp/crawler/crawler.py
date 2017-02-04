# -*- coding: utf-8 -*-
__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event

from bs4 import BeautifulSoup
import re
import urllib2
import datetime


class Crawler():
    def __init__(self):
        self.base_url = "http://www.wikicfp.com"
        self.events_url = self.base_url + "/cfp/allcfp"
        self.max_number_pages = 20

    def get_prop_span(self, a, prop):
        if prop == "text":
            return a.get_text().encode("ascii", "ignore") if a is not None else ""
        else:
            return a[prop].encode("ascii", "ignore") if a is not None else ""

    def crawler(self):
        for number_page in range(1, self.max_number_pages + 1):
            events_url = self.events_url + "?page=" + str(number_page)
            page = urllib2.urlopen(events_url)
            soup = BeautifulSoup(page, "lxml")
            event_urls = soup.findAll('a', href=re.compile('^/cfp/servlet/event.showcfp'))
            for event_url in event_urls:
                event_url = self.base_url + event_url["href"]
                page = urllib2.urlopen(event_url)
                soup2 = BeautifulSoup(page, "lxml")
                event_properties = soup2.findAll('span', typeof=re.compile('v:Event'))
                event = Event()
                for event_property in event_properties:
                    name_property = self.get_prop_span(event_property.find('span', property=re.compile('v:summary')), "content")
                    start_property = self.get_prop_span(event_property.find('span', property=re.compile('v:startDate')), "content")
                    end_property = self.get_prop_span(event_property.find('span', property=re.compile('v:endDate')), "content")
                    type_property = self.get_prop_span(event_property.find('span', property=re.compile('v:eventType')), "content")
                    locality_property = self.get_prop_span(event_property.find('span', property=re.compile('v:locality')), "content")
                    description_property = self.get_prop_span(event_property.find('span', property=re.compile('v:description')), "text")
                    if name_property == 'Submission Deadline':
                        event.submission_deadline = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                    if name_property == 'Notification Due':
                        event.notification_date = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                    if name_property == 'Final Version Due':
                        event.camera_ready = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                    if len(description_property) > 0:
                        event.acronym = name_property
                        event.title_event = description_property
                        event.start_date = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                        event.end_date = datetime.datetime.strptime(end_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                    if len(locality_property) > 0:
                        event.location = locality_property
                    if len(type_property) > 0:
                        event.type_event = type_property
                categories = soup2.findAll("a", href=re.compile('conference'))
                categories_name = []
                for cat in categories:
                    cat_name = self.get_prop_span(cat, "text").encode("utf-8")
                    categories_name.append(cat_name)
                event.categories = ", ".join([c for c in categories_name])
                event.event_url = self.get_prop_span(soup2.find("a", target="_newtab"), "href")
                event.description = self.get_prop_span(soup2.find("div", {"class": "cfp"}), "text")
                print(event.acronym)
                if event.acronym is not None:
                    event.save()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawler()





