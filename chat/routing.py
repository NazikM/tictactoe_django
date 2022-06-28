from django.urls import re_path

from chat.consumers import GameConsumer, LobbyConsumer

websocket_urls = [
    re_path(r'^ws/lobby/$', LobbyConsumer.as_asgi()),
    re_path(r'^ws/game/(?P<room_name>\w+)/$', GameConsumer.as_asgi()),
]