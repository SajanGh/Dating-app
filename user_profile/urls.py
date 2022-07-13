from django.urls import path
from user_profile.views import index, UpdateProfile

urlpatterns = [
    path("", index, name="index"),
    path("profile/update/<str:pk>", UpdateProfile.as_view(), name="update_profile"),
]
