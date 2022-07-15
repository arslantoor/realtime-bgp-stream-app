from django.urls import path
from .consumer import BgpBlackVTFront

ws_urlpatterns = [
    path('ws/<int:user_id>', BgpBlackVTFront.as_asgi()),
    path('ws/<str:user_id>', BgpBlackVTFront.as_asgi()),
]
