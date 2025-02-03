from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from backend.items.models import *
from .models import MainBanner, MainSettings
from .serializers import MainBannerSerializer, PrivacyPolicySerializer
from rest_framework import generics, mixins, viewsets


class MainBannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MainBanner.objects.all()
    serializer_class = MainBannerSerializer


class PrivacyPolicyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MainSettings.objects.all()
    serializer_class = PrivacyPolicySerializer
