# -*- coding: utf-8 -*-
__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event

# import peewee
# from peewee import *
from bs4 import BeautifulSoup
import re
import urllib2
import datetime

#db = MySQLDatabase('sci_cfp_db', user='root', passwd='desarrollo')

"""
class Event(Model):
    acronym = CharField(max_length=500,)
    title_event = CharField(max_length=1000,)
    submission_deadline = DateField()
    event_url = CharField(max_length=1000,)
    end_date = DateField()
    camera_ready = DateField()
    type_event = CharField(max_length=255,)
    notification_date = DateField()
    location = CharField(max_length=500,)
    start_date = DateField()
    categories = CharField(max_length=1000,)

    class Meta:
        database = db
        db_table = "cfp_event"
"""

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
        events = []
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
                # event = dict()
                # Event.create_table()
                event = Event()
                for event_property in event_properties:
                    name_property = self.get_prop_span(event_property.find('span', property=re.compile('v:summary')), "content")
                    start_property = self.get_prop_span(event_property.find('span', property=re.compile('v:startDate')), "content")
                    end_property = self.get_prop_span(event_property.find('span', property=re.compile('v:endDate')), "content")
                    type_property = self.get_prop_span(event_property.find('span', property=re.compile('v:eventType')), "content")
                    locality_property = self.get_prop_span(event_property.find('span', property=re.compile('v:locality')), "content")
                    description_property = self.get_prop_span(event_property.find('span', property=re.compile('v:description')), "text")
                    if name_property == 'Submission Deadline':
                        # event["submission_deadline"] = start_property
                        event.submission_deadline = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else ""
                    if name_property == 'Notification Due':
                        # event["notification_date"] = start_property
                        event.notification_date = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else ""
                    if name_property == 'Final Version Due':
                        # event["camera_ready"] = start_property
                        event.camera_ready = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else ""
                    if len(description_property) > 0:
                        # event["acronym"] = name_property
                        event.acronym = name_property
                        # event["title_event"] = description_property
                        event.title_event = description_property
                        # event["start_date"] = start_property
                        event.start_date = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else ""
                        # event["end_date"] = end_property
                        event.end_date = datetime.datetime.strptime(end_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else ""
                    if len(locality_property) > 0:
                        # event["location"] = locality_property
                        event.location = locality_property
                    if len(type_property) > 0:
                        #event["type_event"] = type_property
                        event.type_event = type_property
                categories = soup2.findAll("a", href=re.compile('conference'))
                categories_name = []
                for cat in categories:
                    cat_name = self.get_prop_span(cat, "text").encode("utf-8")
                    categories_name.append(cat_name)
                # event["categories"] = ", ".join([c for c in categories_name])
                event.categories = ", ".join([c for c in categories_name])
                # event["event_url"] = self.get_prop_span(soup2.find("a", target="_newtab"), "href")
                event.event_url = self.get_prop_span(soup2.find("a", target="_newtab"), "href")
                event.description = self.get_prop_span(soup2.find("div", {"class": "cfp"}), "text")
                # events.append(event)
                print(event.acronym)
                #query = Event.objects(acronym=event.acronym)
                event.save()
        # print(events)
        # with open('data.json', 'w') as fp:
        #    json.dump(events, fp, indent=4)
if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawler()





