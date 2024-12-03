from django.contrib import admin

from .models import MainBanner, MainSettings


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(MainSettings)
class MainBannerAdmin(admin.ModelAdmin):
    pass
