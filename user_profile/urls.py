from django.urls import path
from user_profile.views import index

urlpatterns = [
    path("", index, name="index"),
]
