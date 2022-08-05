from django.shortcuts import render
from django.views.generic import ListView
from user_profile.models import UserProfile


class FilterUser(ListView):
    model = UserProfile
    template_name = "filter_users.html"
