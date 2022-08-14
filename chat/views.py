from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class ChatBoxView(TemplateView):
    template_name = "chatbox.html"
