__author__ = 'laura'
from bs4 import BeautifulSoup
import re
import urllib2
# import json
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sci_cfp.settings
from cfp.models import Event


class Crawler():
    def __init__(self):
        self.base_url = "http://www.wikicfp.com"
        self.events_url = self.base_url + "/cfp/allcfp"
        self.max_number_pages = 20

    def get_prop_span(self, a, prop):
        if prop == "text":
            return a.get_text() if a is not None else ""
        else:
            return a[prop] if a is not None else ""

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
                        event.submission_deadline = start_property
                    if name_property == 'Notification Due':
                        # event["notification_date"] = start_property
                        event.notification_date = start_property
                    if name_property == 'Final Version Due':
                        # event["camera_ready"] = start_property
                        event.camera_ready = start_property
                    if len(description_property) > 0:
                        # event["acronym"] = name_property
                        event.acronym = name_property
                        # event["title_event"] = description_property
                        event.title_event = description_property
                        # event["start_date"] = start_property
                        event.start_date = start_property
                        # event["end_date"] = end_property
                        event.end_date = end_property
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
                # events.append(event)
                event.save()
        # print(events)
        # with open('data.json', 'w') as fp:
        #    json.dump(events, fp, indent=4)
if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawler()





