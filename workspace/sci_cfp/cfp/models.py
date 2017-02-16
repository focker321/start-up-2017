from __future__ import unicode_literals

from django.db import models
from mongoengine import *
# Create your models here.
# db.event.update({}, {$rename:{"location":"city"}}, false, true);

class Event(Document):
    id = StringField(max_length=200, unique=True, primary_key=True)
    acronym = StringField(max_length=200)
    year = IntField(default="0")
    title_event = StringField(max_length=1000, default="")
    sponsored = StringField(max_length=200, default="")
    image = StringField(max_length=200, default="")
    submission_deadline = DateTimeField(default=None, null=True)
    event_url = StringField(max_length=1000, default="")
    end_date = DateTimeField(default=None, null=True)
    camera_ready = DateTimeField(default=None, null=True)
    type_event = StringField(max_length=255, default="")
    notification_date = DateTimeField(default=None, null=True)
    city = StringField(max_length=500, default="")
    country = StringField(max_length=500, default="")
    start_date = DateTimeField(default=None, null=True)
    categories = StringField(max_length=500, default="")
    description = StringField(default="")
    rating = DecimalField(default=0.0)
    city = StringField(max_length=500, default="")
    country = StringField(max_length=500, default="")


class Favorite(Document):
    id = StringField(max_length=200, unique=True, primary_key=True)
    user_id = IntField(default=0)
    event_id = StringField(max_length=200, default="")


class Category(Document):
    id = SequenceField(primary_key=True)
    title = StringField(default="")
    meta = {
        'ordering': ['title']
    }

    def as_json(self):
        return dict(id=self.id, title=self.title)


class Recommendation(Document):
    id = SequenceField(primary_key=True)
    user = StringField(default="0")
    event = StringField(max_length=200, default="")
    prediction = DecimalField(default=0.0)


class ProfileEvent(Document):
    id = SequenceField(primary_key=True)
    event = StringField(max_length=200, default="")
    type = StringField(max_length=200, default="")
    feature = StringField(max_length=200, default="")
    feature_value = DecimalField(default=0.0)
    feature_order = IntField(default=0)
    meta = {
        'ordering': ['feature_order']
    }


class Interest(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField(default=0)
    category_id = IntField(default=0)
