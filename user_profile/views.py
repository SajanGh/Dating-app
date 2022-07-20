from django import dispatch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from user_profile.models import User, UserProfile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from DatingAppProject.decorators import profile_update_required

decorators = [login_required, profile_update_required]


@method_decorator(decorators, name="dispatch")
class Index(ListView):
    model = UserProfile
    template_name = "index.html"


@method_decorator(login_required, name="dispatch")
class UpdateProfile(UpdateView):
    model = UserProfile
    template_name = "profile/update_profile.html"
    success_url = reverse_lazy("index")
    fields = [
        "first_name",
        "last_name",
        "bio",
        "date_of_birth",
        "address",
        "phone",
        "gender",
        "looking_for",
        "profile_picture",
    ]
