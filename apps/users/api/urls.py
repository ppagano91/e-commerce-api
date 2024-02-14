from django.urls import path
from apps.users.api.api import user_api_view

urlpatterns = [
    path('all/', user_api_view, name='users_api'),
]