from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from user_profile.models import UserProfile
from find_users.filters import UserFilter
from .utilities import calculate_distance


def FilterUser(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        if request.method == "POST":
            f = UserFilter(request.POST, queryset=UserProfile.objects.all())
            return render(request, "filter_users_list.html", {"filter": f})
        else:
            return JsonResponse({"status": "Invalid Request"}, status=400)
    else:
        f = UserFilter(request.GET, queryset=UserProfile.objects.all())
        return render(request, "filter_users.html", {"filter": f, "title": "Filter"})


def get_users_by_raduis(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        if request.method == "GET":
            range = request.GET.get("range")
            querylist = [
                x
                for x in UserProfile.objects.exclude(user=request.user)
                if calculate_distance(request.user, x.lat, x.long) <= int(range)
            ]
            return render(
                request, "swipe_users_ajax.html", {"userprofile_list": querylist}
            )
        else:
            return JsonResponse({"status": "Invalid Request"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid Request")
