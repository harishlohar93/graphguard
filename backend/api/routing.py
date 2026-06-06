from django.urls import path
from api.consumer import AlertConsumer

websocket_urlpatterns = [
    path("ws/alerts/", AlertConsumer.as_asgi()),
]