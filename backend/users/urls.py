from django.urls import path

from .views import *
from rest_framework import routers

from .views import UserRegisterViewSet

user_router = routers.DefaultRouter()

user_router.register(r"registry", UserRegisterViewSet, basename="registry")
