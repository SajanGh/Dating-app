from django.urls import path
from user_profile.views import Index, UpdateProfile

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("profile/update/<str:pk>", UpdateProfile.as_view(), name="update_profile"),
]
