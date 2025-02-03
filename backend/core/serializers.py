from rest_framework import serializers

from backend.items.models import Like
from .models import MainBanner, MainSettings


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = ("id", "title", "text", "button_link", "order", "background_image")


class LikeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Like
        fields = ("product",)


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSettings
        fields = ("id", "privacy_policy")
