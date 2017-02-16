__author__ = 'laura'
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sci_cfp import settings
from mongoengine import *
from cfp.models import Event, Category, ProfileEvent, Favorite


class BuilderData():
    @staticmethod
    def build_categories():
        events = Event.objects(Q(rating=0.0))
        for event in events:
            categories = event.categories.split(",")
            for cat_name in categories:
                if len(cat_name) > 0 and "http" not in cat_name:
                    cat_name = cat_name.lower().strip()
                    category_exists = Category.objects(Q(title=cat_name))
                    if len(category_exists) == 0:
                        category = Category()
                        category.title = cat_name
                        category.save()
            event.rating = 1.0
            event.save()
        print(len(Category.objects()))

    @staticmethod
    def build_profile_item():
        categories = Category.objects()
        events = Event.objects()
        for event in events:
            for idx, category in enumerate(categories):
                feature_value = 0
                if category.title in event.categories:
                    feature_value = 1
                profile_event = ProfileEvent()
                profile_event.event = event.id
                profile_event.type = "category"
                profile_event.feature = category.title
                profile_event.feature_value = feature_value
                profile_event.feature_order = idx + 100
                profile_event.save()
    @staticmethod
    def recommender():
        favorites = Favorite().objects()
        with open("ratings"+".txt", 'w') as f:
            for favorite in favorites:
                row = "%s,%s,%i" % (favorite.user, favorite.event, 1)
                f.write(row + '\n')
        events = Event().objects()
        with open("items"+".txt", 'w') as f:
            for event in events:
                row = event.id + ","
                profile_events = ProfileEvent().objects(event.id)
                row += "|".join(profile_event.feature_value for profile_event in profile_events)
            f.write(row + '\n')

#BuilderData.build_categories()
BuilderData.build_profile_item()
#BuilderData.recommender()

        




