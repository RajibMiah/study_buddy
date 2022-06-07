import base.routing
import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            *chat.routing.websocket_urlpatterns,
            *base.routing.websocket_urlpatterns,
           ])
    ),
})
