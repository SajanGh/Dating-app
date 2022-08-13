from django.urls import path
from user_profile.views import (
    Index,
    UpdateProfile,
    rightSwipeUser,
    list_user_notifications,
    UserDetailView,
    AddUserInterest,
    UpdateUserDescription,
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("profile/update/<str:pk>", UpdateProfile.as_view(), name="update_profile"),
    path("profile/detail/<str:pk>", UserDetailView.as_view(), name="profile_detail"),
    path("right_swipe/", rightSwipeUser, name="right_swipe"),
    path("matches/", list_user_notifications, name="matches"),
    path("add/interests/", AddUserInterest.as_view(), name="add_interest"),
    path(
        "profile/description/<str:pk>",
        UpdateUserDescription.as_view(),
        name="update_description",
    ),
]
