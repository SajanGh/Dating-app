from django.shortcuts import render
from user_profile.models import UserDescription, UserProfile
from find_users.filters import UserFilter


# class FilterUser(ListView):
#     model = UserProfile
#     template_name = "filter_users.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form1"] = UserDescriptionForm()
#         context["form2"] = UserFilterForm()
#         return context


def FilterUser(request):
    print(request.GET.get("zodiac"))
    f = UserFilter(request.GET, queryset=UserProfile.objects.all())
    print(f.qs)
    return render(request, "filter_users.html", {"filter": f})
