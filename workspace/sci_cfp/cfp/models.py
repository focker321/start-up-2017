from __future__ import unicode_literals

from django.db import models
from mongoengine import *
# Create your models here.


class Event(Document):
    acronym = StringField(max_length=200, unique=True, primary_key=True)
    title_event = StringField(max_length=1000, default="")
    submission_deadline = DateTimeField(default=None, null=True)
    event_url = StringField(max_length=1000, default="")
    end_date = DateTimeField(default=None, null=True)
    camera_ready = DateTimeField(default=None, null=True)
    type_event = StringField(max_length=255, default="")
    notification_date = DateTimeField(default=None, null=True)
    location = StringField(max_length=500, default="")
    start_date = DateTimeField(default=None, null=True)
    categories = StringField(max_length=500, default="")
    description = StringField(default="")

    #def __str__(self):
    #    return self.acronym

    # class Meta:
    #    database = db