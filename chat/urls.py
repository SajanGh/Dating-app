import imp
from django.urls import path
from chat.views import ChatBoxView

urlpatterns = [
    path("", ChatBoxView.as_view(), name="chatbox"),
]
