__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event

from crawler import Crawler
from bs4 import BeautifulSoup
import re
import urllib2
import datetime


class CrawlerEvent(Crawler):
    def __init__(self):
        self.base_url = "http://www.wikicfp.com"
        self.events_url = self.base_url + "/cfp/allcfp"
        self.search = self.base_url + "/cfp/servlet/tool.search"
        self.max_number_pages = 20

    def crawler_page(self, number_page):
        events_url = self.events_url + "?page=" + str(number_page)
        page = urllib2.urlopen(events_url)
        soup = BeautifulSoup(page, "lxml")
        event_urls = soup.findAll('a', href=re.compile('^/cfp/servlet/event.showcfp'))
        for event_url in event_urls:
            event = self.crawler_element(event_url)
            if event is not None:
                event.save()

    def crawler_search(self, acronym):
        event = None
        events_url = self.search + "?q=" + acronym + "&year=t"
        page = urllib2.urlopen(events_url)
        soup = BeautifulSoup(page, "lxml")
        event_urls = soup.findAll('a', href=re.compile('^/cfp/servlet/event.showcfp'))
        for event_url in event_urls:
            event = self.crawler_element(event_url)
            if event is not None and event.acronym == acronym:
                event.save()
                break
        return event

    def crawler_element(self, event_url):
        result = None
        event_url = self.base_url + event_url["href"]
        page = urllib2.urlopen(event_url)
        if page is not None:
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
                    event.id = name_property.replace(" ", "").strip().lower()
                    event.acronym = name_property[:-5].replace("ACM", "").replace("IEEE", "").strip()
                    event.year = int(name_property[-4:])
                    event.title_event = description_property.split(':')[1].strip()
                    event.start_date = datetime.datetime.strptime(start_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None
                    event.end_date = datetime.datetime.strptime(end_property, "%Y-%m-%dT%H:%M:%S").date() if len(start_property) > 0 else None

                    if "ACM" in name_property:
                        event.sponsored = "ACM"
                    elif "IEEE" in name_property:
                        event.sponsored = "IEEE"
                    else:
                        event.sponsored = ""
                if len(locality_property) > 0:
                    event.location = locality_property
                    if os.path.isfile('../cfp/static/cfp/img/'+ locality_property.replace(" ", "").lower() +'.png'):
                        event.image = '/static/cfp/img/' + locality_property.replace(" ", "").lower() + '.png'
                    else:
                        event.image = '/static/cfp/img/none.png'
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
            if event.acronym is not None:
                result = event
        else:
            print("Page of event not retrieved")
        return result

    def retrieve_event(self, acronym, title):
        try:
            event = Event.objects().get(acronym=acronym)
            print("RETRIEVED EVENT ID %s" % event.id)
        except Event.DoesNotExist:
            event_id = acronym.replace(" ", "").strip().lower()
            event = self.crawler_search(event_id)
            if event is None:
                event = Event()
                event.id = event_id
                event.acronym = acronym
                event.title_event = title
                event.save()
                print("CREATED EVENT ID! %s" % event.id)
            else:
                print("SEARCHED EVENT ID! %s" % event.id)
        return event


if __name__ == '__main__':
    crawler_event = CrawlerEvent()
    crawler_event.crawler()