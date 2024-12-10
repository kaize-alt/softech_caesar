from django.contrib import admin
from .models import Cart, CartItem, Category, Product, SubCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ["id", "product", "cart", "amount", "total_price",]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
