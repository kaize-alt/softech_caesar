from rest_framework import serializers

from backend.items.models import Like

from .models import MainBanner


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = ("id", )

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('product', )
