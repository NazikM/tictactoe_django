from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.routing import websocket_urls

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter(
        websocket_urls
    ))
})
