from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "date_joined",
        "id",
    )
