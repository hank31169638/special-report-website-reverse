from django.contrib import admin
from django.urls import path, include
from .views import GoodsView

urlpatterns = [
    path("get-goods", GoodsView.as_view()),
]
