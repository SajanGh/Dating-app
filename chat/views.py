from concurrent.futures import thread
from multiprocessing import context
from django.shortcuts import render
from chat.models import PrivateChatThread, PrivateChatMessage
from user_profile.models import UserProfile, UserConnection
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def ChatBoxView(request):
    logged_in_user = User.objects.values("id", "email").get(id=request.user.id)

    connections = UserConnection.objects.filter(owner=request.user.profile).first()

    context = {
        "connections": connections,
        "logged_in_user": logged_in_user,
    }
    return render(request, "chatbox.html", context)


def get_private_chat(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        user_1 = request.user
        user_2 = request.GET.get("user_2", None)
        user_2_instance = User.objects.filter(id=user_2).first()
        print(user_2)
        private_chat_thread = PrivateChatThread.objects.get_private_chat_thread(
            user_1,
            user_2_instance,
        )
        if not private_chat_thread:
            private_chat_thread = PrivateChatThread.objects.create(
                user_1=user_1,
                user_2=user_2_instance,
            )
            private_chat_thread.save()
        print(private_chat_thread)
        messages = PrivateChatMessage.objects.get_all_messages(
            chat_thread=private_chat_thread
        )
        context = {
            "thread_messages": messages,
        }
        return render(request, "chat_messages.html", context)
