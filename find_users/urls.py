from django.urls import path
from find_users.views import FilterUser


urlpatterns = [
    path("users/", FilterUser.as_view(), name="filter_user"),
]
