from django.db import models
import uuid
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from user_profile.models import UserProfile, UserDescription, UserInterest
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import requests
import json


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            last_login=timezone.now(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(user_signed_up)
def create_user_profile_instance(user, sociallogin=None, **kwargs):
    UserProfile.objects.create(user=user)
    UserDescription.objects.create(user=user)
    UserInterest.objects.create(user=user)
    if sociallogin:
        if sociallogin.account.provider == "google":
            user.profile.first_name = sociallogin.account.extra_data["given_name"]
            user.profile.last_name = sociallogin.account.extra_data["family_name"]
            user.profile.save()


@receiver(user_logged_in)
def updateLocation(user, **kwargs):
    ip = requests.get("https://api.ipify.org?format=json")
    ip_data = json.loads(ip.text)
    res = requests.get("http://ip-api.com/json/" + ip_data.get("ip"))
    location_data = json.loads(res.text)
    user.profile.long = location_data.get("lon")
    user.profile.lat = location_data.get("lat")
    user.profile.save()
