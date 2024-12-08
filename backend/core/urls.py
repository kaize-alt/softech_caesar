from django.urls import path
from .views import *
from rest_framework import routers
from .views import MainBannerViewSet

urlpatterns = [
    path('', home),
    path('about/', about),
]

core_router = routers.DefaultRouter()

core_router.register(r"main_banner", MainBannerViewSet, basename="category")
core_router.register(r"privacy_policy", PrivacyPolicyViewSet, basename="privacy_policy")


