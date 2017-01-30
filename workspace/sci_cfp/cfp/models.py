from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Event(models.Model):
    acronym = models.CharField(max_length=500,)
    title_event = models.CharField(max_length=1000,)
    submission_deadline = models.DateField()
    event_url = models.CharField(max_length=1000,)
    end_date = models.DateField()
    camera_ready = models.DateField()
    type_event = models.CharField(max_length=255,)
    notification_date = models.DateField()
    location = models.CharField(max_length=500,)
    start_date = models.DateField()
    categories = models.CharField(max_length=1000,)

    def __str__(self):
        return self.acronym