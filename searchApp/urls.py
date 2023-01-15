from django.contrib import admin
from django.urls import path,include
from .view import ListRepo,ClearCatch

urlpatterns = [
    path('search/', ListRepo.as_view()),
    path('clear_caches/', ClearCatch.as_view())
]