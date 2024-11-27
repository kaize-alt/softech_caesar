from django.db import models
from django.contrib.postgres.fields import JSONField

from backend.users.models import CustomUser 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,

        null=True,
        blank=True,
        related_name='subcategories'
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    specifications = models.JSONField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return self.user.username


class  CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_item")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    amount = models.PositiveIntegerField("Кол-во", default=1)
    total_price = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=3, default=0)

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукт в корзине"

    def __str__(self):
        return self.product.name

class Like(models.Model):
    user = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    is_like = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return self.user
