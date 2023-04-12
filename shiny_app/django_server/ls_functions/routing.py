"""Urls for ls_function app"""
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/ls_functions/", consumers.LsFunctionsConsumer.as_asgi()),
]