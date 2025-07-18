"""
ASGI config for educa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')

# ? defining the main ASGI app that will be executed when serving the django product through ASGI
django_asgi_app = get_asgi_application()

# ? below app instantiation to ensure app registry is populated
from chat.routing import websocket_urlpatterns

# ? Channels as the main entry point of routing system
# ? ProtocolTypeRouter takes communication types like http or websocket to ASGI applications
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
        )
    )
})
