from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from DatingAppProject.decorators import profile_update_required


@login_required
@profile_update_required
def index(request):
    context = {}
    return render(request, "index.html", context)


def create_profile(request):
    pass


@login_required
def update_profile(request):
    return HttpResponse("UPDATE PROFILE FIRST")
