from django.db import models
from ckeditor.fields import RichTextField

from backend.users.models import CustomUser 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField("Иконка подкатегории", upload_to="icon_subcategory")
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегория"

    def __str__(self):
        return f"{self.category.name}, {self.name}"

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    description = RichTextField("Описание Товара", blank=True, null=True)
    price = models.DecimalField("Цена Товара", blank=True, null=True, max_digits=10, decimal_places=3)
    full_desc = RichTextField("Полное описание Товара", blank=True, null=True)
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукт"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField("Картинки Товара")

    class Meta:
        verbose_name = "Картинка продукта"
        verbose_name_plural = "Картинки продуктов"

    def __str__(self):
        return f"Image for {self.product.name}"


    
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    is_like = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
