import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles normal HTTP requests
    "websocket": URLRouter(chat.routing.websocket_urlpatterns),  # Handles WebSockets
})
