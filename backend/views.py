from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from openai import OpenAI
import json
import requests


def home(request):
    return render(request, "characterSelection.html")


def chat(request):
    return render(request, "chat.html")


def story(request):
    return render(request, "story.html")
