from django.urls import re_path
from . import consumers


# ! Channels' URL routing may not function correctly with path() routes if inner routers are wrapped by additional middleware
# ? as_asgi() instantiate a cousmer that each user is connecting to
websocket_urlpatterns = [
    re_path(
        r'ws/chat/room/(?P<course_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]
