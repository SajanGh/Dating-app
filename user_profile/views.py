from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from requests import request
from user_profile.models import UserProfile, Heart
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from DatingAppProject.decorators import profile_update_required


decorators = [login_required, profile_update_required]


@method_decorator(decorators, name="dispatch")
class Index(ListView):
    model = UserProfile
    template_name = "index.html"

    def get_queryset(self):
        queryset = UserProfile.objects.exclude(user=self.request.user)
        return queryset


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


@login_required
def rightSwipeUser(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        if request.method == "POST":
            receiver_id = request.POST.get("receiver")
            receiver = UserProfile.objects.filter(id=receiver_id).first()
            data = {}
            if receiver == request.user.profile:
                data["message"] = "You cannot sent heart to yourself."
                return JsonResponse(data)
            data["message"] = "Heart successfully sent."
            Heart.objects.create(sent_by=request.user.profile, received_by=receiver)
            return JsonResponse(data)
        else:
            return HttpResponseBadRequest("Invalid Request", status=400)
    else:
        return HttpResponseBadRequest("Invalid Request.")
