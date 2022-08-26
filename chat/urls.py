import imp
from django.urls import path
from chat.views import ChatBoxView, get_private_chat, get_shared_key

urlpatterns = [
    path("", ChatBoxView, name="chatbox"),
    path("get_messages/", get_private_chat, name="get_private_chat"),
    path("get_shared_key/", get_shared_key, name="get_shared_key"),
]
