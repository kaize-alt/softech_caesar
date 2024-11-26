from django.urls import path

from .views import *

urlpatterns = [
    path('users/<slug:users_page>/', usersIndex),
]
