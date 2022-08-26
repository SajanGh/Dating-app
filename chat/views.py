from telnetlib import STATUS
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from chat.models import PrivateChatThread, PrivateChatMessage
from user_profile.models import UserConnection, Key
from DatingAppProject.diffie_hellman import DiffieHellman
from django.contrib.auth import get_user_model

User = get_user_model()


def ChatBoxView(request):
    logged_in_user = User.objects.values("id", "email").get(id=request.user.id)
    print(logged_in_user)

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
        messages = PrivateChatMessage.objects.get_all_messages(
            chat_thread=private_chat_thread
        )
        context = {
            "thread_messages": messages,
        }
        return render(request, "chat_messages.html", context)
    else:
        return HttpResponseBadRequest("Invalid request")


def get_shared_key(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        data = {}
        public_key = request.GET.get("p_key")
        user = request.user
        qs = Key.objects.filter(keys_owner=user).first()
        local_private_key = qs.private_key
        if qs.keys_owner != user:
            return JsonResponse({"status": "You are not Allowed"}, status=400)
        shared_key = DiffieHellman.generate_shared_key_static(
            local_private_key, public_key
        )
        data["s_key"] = shared_key
        return JsonResponse(data, status=200)
    else:
        return HttpResponseBadRequest("Invalid request")
