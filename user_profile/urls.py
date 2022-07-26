from django.urls import path
from user_profile.views import Index, UpdateProfile, rightSwipeUser

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("profile/update/<str:pk>", UpdateProfile.as_view(), name="update_profile"),
    path("right_swipe/", rightSwipeUser, name="right_swipe"),
]
