import datetime
import os
import uuid

import math
from django.db.models.expressions import RawSQL
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from bisect import bisect
from django.conf import settings
from django.db import models

from common.constants import (
    HEIGHT,
    LOOKING_FOR_CHOICES,
    GENDER_CHOICES,
    signs,
    ZODIAC_CHOICES,
    HAIR_COLOUR,
    HAIR_LENGTH,
    BODY_TYPE,
    RELIGION,
    RELATIONSHIP_STATUS,
    EDUCATION,
    EYE_COLOR,
    HEIGHT,
)
from common.models import CommonInfo


User = settings.AUTH_USER_MODEL


# Renames user uploaded images
def path_and_rename(instance, filename):
    upload_to = "media/profile_images"
    ext = filename.split(".")[-1]

    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        filename = "{}.{}".format(uuid.uuid4().hex, ext)
    return os.path.join(upload_to, filename)


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    cf = connection.connection.create_function
    cf("acos", 1, math.acos)
    cf("cos", 1, math.cos)
    cf("radians", 1, math.radians)
    cf("sin", 1, math.sin)


class LocationManager(models.Manager):

    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, citylat, citylong, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        gcd_formula = "6371 * acos(cos(radians(%s)) * \
        cos(radians(citylat)) \
        * cos(radians(citylong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(citylat)))"
        distance_raw_sql = RawSQL(gcd_formula, (citylat, citylong, citylat))

        if max_distance is not None:
            return self.annotate(distance=distance_raw_sql).filter(
                distance__lt=max_distance
            )
        else:
            return self.annotate(distance=distance_raw_sql)


# Profile model for user-- contains personal information
class UserProfile(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(max_length=100, default="", blank=False)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, default="MALE")

    profile_picture = models.ImageField(upload_to=path_and_rename, null=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    age = models.IntegerField(null=True, blank=True)
    zodiac = models.CharField(
        choices=ZODIAC_CHOICES, max_length=15, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.age = self.get_age()
        self.zodiac = self.get_zodiac()
        super(UserProfile, self).save(*args, **kwargs)

    def get_age(self):
        return int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)

    def get_zodiac(self):
        month = int(self.date_of_birth.strftime("%m"))
        day = int(self.date_of_birth.strftime("%d"))
        return signs[bisect(signs, (month, day))][2]

    def __str__(self):
        return self.user.email


class UserDescription(CommonInfo):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="description"
    )
    height = models.CharField(choices=HEIGHT, default="4 to 5", max_length=10)
    eye_color = models.CharField(choices=EYE_COLOR, max_length=10, default="BLACK")
    hair_length = models.CharField(
        choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100
    )
    hair_colour = models.CharField(
        choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10
    )
    body_type = models.CharField(
        choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15
    )
    religion = models.CharField(
        choices=RELIGION, default="HINDU", blank=False, max_length=100
    )
    relationship_status = models.CharField(
        choices=RELATIONSHIP_STATUS, default="SINGLE", blank=False, max_length=100
    )
    education = models.CharField(
        choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100
    )
    looking_for = models.CharField(
        choices=LOOKING_FOR_CHOICES, max_length=6, default="BOTH"
    )
    is_completed = models.BooleanField(default=False)


class UserInterest(CommonInfo):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="interest"
    )
    title = models.CharField(max_length=20, blank=True, null=True)


class UserConnection(CommonInfo):
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="connections"
    )
    user = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.owner.user.email


class Heart(CommonInfo):
    sent_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="heart_sender"
    )
    received_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="heart_receiver"
    )
