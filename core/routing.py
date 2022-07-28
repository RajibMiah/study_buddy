import base.routing
# import chat.routing
import chat.ws_urls
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # *chat.routing.websocket_urlpatterns,
            *base.routing.websocket_urlpatterns,
            *chat.ws_urls.websocket_urlpatterns
        ])
    ),
})
