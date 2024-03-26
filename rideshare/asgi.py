"""
ASGI config for rideshare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from rides.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rideshare.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : URLRouter(websocket_urlpatterns),
})
