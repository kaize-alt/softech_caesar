from django.contrib import admin
from .models import Category, SubCategory, Product, Review, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    search_fields = ['name', 'category__name']
    list_filter = ['category']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'price', 'get_average_rating']
    search_fields = ['name', 'subcategory__name']
    list_filter = ['subcategory', 'price']
    ordering = ['name']

    @admin.display(description="Средний рейтинг")
    def get_average_rating(self, obj):
        return obj.average_rating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username']


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ["id", "product", "cart", "amount", "total_price"]
    readonly_fields = ["id", "total_price"]
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
