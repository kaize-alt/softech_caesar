from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator

from backend.users.models import CustomUser 


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    image = models.ImageField("Иконка подкатегории", upload_to="icon_subcategory")
    description = RichTextField(verbose_name="Описание категории", blank=True, null=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.category.name}, {self.name}"


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    description = RichTextField(verbose_name="Описание товара", blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена товара", max_digits=10, decimal_places=2, null=True, blank=True)
    full_desc = RichTextField(verbose_name="Полное описание товара", blank=True, null=True)
    total_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return round(self.total_rating / self.rating_count, 2) if self.rating_count > 0 else 0


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            old_review = Review.objects.get(pk=self.pk)
            self.product.total_rating -= old_review.rating
        self.product.total_rating += self.rating
        if is_new:
            self.product.rating_count += 1
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.total_rating -= self.rating
        self.product.rating_count = max(0, self.product.rating_count - 1)
        self.product.save()
        super().delete(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField("Картинка товара", upload_to="product_images")

    class Meta:
        verbose_name = "Картинка продукта"
        verbose_name_plural = "Картинки продуктов"

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    amount = models.PositiveIntegerField("Кол-во", default=1)
    total_price = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

    def __str__(self):
        return f"{self.amount} x {self.product.name}"

    def save(self, *args, **kwargs):
        self.total_price = self.amount * (self.product.price or 0)
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="liked_products")
    is_like = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
