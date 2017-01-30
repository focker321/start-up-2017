from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Event(models.Model):
    acronym = models.CharField(max_length=200, unique=True, primary_key=True)
    title_event = models.CharField(max_length=1000, default="")
    submission_deadline = models.DateField(default=None, null=True)
    event_url = models.CharField(max_length=1000, default="")
    end_date = models.DateField(default=None, null=True)
    camera_ready = models.DateField(default=None, null=True)
    type_event = models.CharField(max_length=255, default="")
    notification_date = models.DateField(default=None, null=True)
    location = models.CharField(max_length=500, default="")
    start_date = models.DateField(default=None, null=True)
    categories = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.acronym

    # class Meta:
    #    database = db