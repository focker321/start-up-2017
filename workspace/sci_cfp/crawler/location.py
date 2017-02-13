# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event

import json
import requests

url = 'http://api.geonames.org/searchJSON?maxRows=1&username=scicfp'
# db.event.update({}, {$rename:{"location":"city"}}, false, true);

events = Event.objects.all()

for e in events:
    if len(e.city.split()) > 0:
        q_city = e.city.split()[0].replace(',', '').replace('\n', '')
        result = requests.get(url+'&q='+q_city)
        result = json.loads(result.content)
        print q_city
        if len(result['geonames']) > 0:
            city = ''
            country = ''
            if 'name' in result['geonames'][0].keys():
                city = result['geonames'][0]['name']
            if 'countryName' in result['geonames'][0].keys():
                country = result['geonames'][0]['countryName']
            print '\t', city.encode('utf-8'), country.encode('utf-8')
            e.city = city
            e.country = country
            e.save()

