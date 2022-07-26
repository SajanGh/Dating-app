import datetime
from operator import mod
import os
import uuid
from bisect import bisect
from django.conf import settings
from django.db import models
from django.dispatch import receiver

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


# Profile model for user-- contains personal information
class UserProfile(models.Model):

    GENDER_CHOICES = [("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other")]
    LOOKING_FOR_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("BOTH", "Both"),
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(max_length=100, default="", blank=False)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, default="MALE")
    looking_for = models.CharField(
        choices=LOOKING_FOR_CHOICES, max_length=6, default="BOTH"
    )
    profile_picture = models.ImageField(upload_to=path_and_rename, null=True)

    def age(self):
        return int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)

    def zodiac(self):
        signs = [
            (1, 20, "Capricorn"),
            (2, 18, "Aquarius"),
            (3, 20, "Pisces"),
            (4, 20, "Aries"),
            (5, 21, "Taurus"),
            (6, 21, "Gemini"),
            (7, 22, "Cancer"),
            (8, 23, "Leo"),
            (9, 23, "Virgo"),
            (10, 23, "Libra"),
            (11, 22, "Scorpio"),
            (12, 22, "Sagittarius"),
            (12, 31, "Capricorn"),
        ]
        month = int(self.date_of_birth.strftime("%m"))
        day = int(self.date_of_birth.strftime("%d"))
        return signs[bisect(signs, (month, day))][2]

    def __str__(self):
        # return self.first_name + " " + self.last_name
        return self.user.email


class Heart(models.Model):
    sent_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="heart_sender"
    )
    received_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="heart_receiver"
    )
    created_on = models.DateTimeField(auto_now_add=True)
