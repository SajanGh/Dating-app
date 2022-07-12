from django.urls import path
from user_profile.views import index, update_profile

urlpatterns = [
    path("", index, name="index"),
    path("profile/update/", update_profile, name="update_profile"),
]
