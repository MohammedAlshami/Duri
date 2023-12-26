from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from openai import OpenAI
import json
import requests


def home(request):
    return render(request, "characterSelection.html")