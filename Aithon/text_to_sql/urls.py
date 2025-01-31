from django.urls import path, include
from .views import get_messages_by_thread ,  create_or_update_interaction


urlpatterns = [
    path("messages/<str:thread_id>/", get_messages_by_thread, name="get_messages_by_thread"),
    path("interaction/" ,  create_or_update_interaction , name=" create_or_update_interaction")
]
