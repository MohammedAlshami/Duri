from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.home),
    path("chat", views.chat),
    path("story", views.story),
]
