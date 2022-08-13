import imp
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from user_profile.models import UserProfile
from find_users.filters import UserFilter


def FilterUser(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        if request.method == "POST":
            f = UserFilter(request.POST, queryset=UserProfile.objects.all())
            return render(request, "filter_users_list.html", {"filter": f})
        else:
            return HttpResponseBadRequest("Invalid Request", status=400)
    else:
        f = UserFilter(request.GET, queryset=UserProfile.objects.all())
        return render(request, "filter_users.html", {"filter": f})
