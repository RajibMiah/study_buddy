"""
ASGI config for the Study Buddy project.

Exposes the ASGI callable as a module-level variable named ``application`` and
wires HTTP through Django while routing WebSocket traffic through Channels.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialise Django before importing anything that touches the ORM / settings.
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import (  # noqa: E402
    AllowedHostsOriginValidator,
)

import base.routing  # noqa: E402
import chat.ws_urls  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        *base.routing.websocket_urlpatterns,
                        *chat.ws_urls.websocket_urlpatterns,
                    ]
                )
            )
        ),
    }
)
