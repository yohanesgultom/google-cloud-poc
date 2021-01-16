from django.urls import path, re_path

from .views import (
    index,
    action,
    messages,
    publish,
)

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^action/?$', action, name='action'),
    re_path(r'^messages/?$', messages, name='messages'),
    re_path(r'^publish/?$', publish, name='publish'),
]
