from django.contrib import admin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "date_joined",
        "id",
    )
