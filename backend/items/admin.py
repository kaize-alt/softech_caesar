from django.contrib import admin
from django.db.models import JSONField, TextField
from django.forms import Textarea
from .models import Category, Brand, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)
    empty_value_display = '-пусто-'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    empty_value_display = '-пусто-'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'in_stock', 'created_at', 'get_specifications')
    search_fields = ('name', 'category__name', 'brand__name')
    list_filter = ('category', 'brand', 'in_stock')
    ordering = ('-created_at',)
    autocomplete_fields = ('category', 'brand')
    readonly_fields = ('created_at', 'updated_at')
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': ('name', 'category', 'brand', 'price', 'description', 'image', 'in_stock')}),
        ('Advanced Options', {'fields': ('specifications',)}),
    )
    formfield_overrides = {
        JSONField: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
        TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 60})},
    }

    def get_specifications(self, obj):
        import json
        return json.dumps(obj.specifications, indent=2) if obj.specifications else '-'
    get_specifications.short_description = "Specifications"
