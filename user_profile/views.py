from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from user_profile.models import UserDescription, UserProfile, Heart, UserInterest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from DatingAppProject.decorators import profile_update_required
from notifications.signals import notify

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
            Heart.objects.create(
                sent_by=request.user.profile,
                received_by=receiver,
            )
            notify.send(request.user, recipient=receiver.user, verb="Sent you a heart.")
            return JsonResponse(data)
        else:
            return HttpResponseBadRequest("Invalid Request", status=400)
    else:
        return HttpResponseBadRequest("Invalid Request.")


@login_required
@profile_update_required
def list_user_notifications(request):

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        notifications = request.user.notifications.all()
        context = {
            "notifications": notifications,
        }
        return render(request, "profile/list_notifications.html", context)
    else:
        if request.method == "GET":
            notifications = request.user.notifications.all()
            context = {
                "notifications": notifications,
            }
            return render(request, "profile/base_notifications.html", context)


class UserDetailView(DetailView):
    model = UserProfile
    template_name = "profile/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hearts_received"] = Heart.objects.filter(
            received_by=self.kwargs.get("pk")
        )
        context["hearts_sent"] = Heart.objects.filter(sent_by=self.kwargs.get("pk"))
        context["interests"] = UserInterest.objects.filter(user=self.kwargs.get("pk"))
        return context


class AddUserInterest(CreateView):
    model = UserInterest
    fields = ["title"]
    template_name = "profile/user_detail.html"

    def get_success_url(self):
        pk = self.request.user.profile.id
        return reverse_lazy("profile_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)


class UpdateUserDescription(UpdateView):
    model = UserDescription
    fields = [
        "height",
        "eye_color",
        "hair_length",
        "hair_colour",
        "body_type",
        "religion",
        "relationship_status",
        "education",
    ]
    template_name = "profile/update_user_description.html"

    def get_success_url(self):
        pk = self.request.user.profile.id
        return reverse_lazy("profile_detail", kwargs={"pk": pk})
