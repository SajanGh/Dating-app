import datetime
import uuid
from bisect import bisect
from django.conf import settings
from django.db import models

# from django.contrib.auth import get_user_model

# User = get_user_model()
User = settings.AUTH_USER_MODEL


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

    def age(self):
        return int((datetime.datetime.now() - self.date_of_birth).days / 365.25)

    def zodiac(self):
        signs = [
            (1, 20, "Cap"),
            (2, 18, "Aqu"),
            (3, 20, "Pis"),
            (4, 20, "Ari"),
            (5, 21, "Tau"),
            (6, 21, "Gem"),
            (7, 22, "Can"),
            (8, 23, "Leo"),
            (9, 23, "Vir"),
            (10, 23, "Lib"),
            (11, 22, "Sco"),
            (12, 22, "Sag"),
            (12, 31, "Cap"),
        ]
        month = self.date_of_birth.strftime("%m")
        day = self.date_of_birth.strftime("%d")
        return signs[bisect(signs, (month, day))][2]

    def __str__(self):
        # return self.first_name + " " + self.last_name
        return self.user.email
