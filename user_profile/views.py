from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from user_profile.models import UserProfile
from django.contrib.auth.decorators import login_required
from DatingAppProject.decorators import profile_update_required


@login_required
@profile_update_required
def index(request):
    context = {}
    return render(request, "index.html", context)


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
    ]
