from django.urls import path
from user_profile.views import (
    Index,
    UpdateProfile,
    rightSwipeUser,
    list_user_notifications,
    UserDetailView,
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("profile/update/<str:pk>", UpdateProfile.as_view(), name="update_profile"),
    path("profile/detail/<str:pk>", UserDetailView.as_view(), name="profile_detail"),
    path("right_swipe/", rightSwipeUser, name="right_swipe"),
    path("matches/", list_user_notifications, name="matches"),
]
