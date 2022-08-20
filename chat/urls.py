import imp
from django.urls import path
from chat.views import ChatBoxView, get_private_chat

urlpatterns = [
    path("", ChatBoxView, name="chatbox"),
    path("get_messages/", get_private_chat, name="get_private_chat"),
]
