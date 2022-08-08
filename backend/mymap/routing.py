from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:conversation_id>/', consumers.ConversationConsumer.as_asgi()),
]