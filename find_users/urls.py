from django.urls import path
from find_users.views import FilterUser


urlpatterns = [
    path("users/", FilterUser, name="filter_user"),
]
