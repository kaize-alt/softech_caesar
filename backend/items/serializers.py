from rest_framework import serializers
from django.db.models import F
from .models import Category, SubCategory, Product, ProductImage, Review, CartItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "image")


class ProductSerializerList(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "price", "image", "average_rating", "created_at")

    def get_average_rating(self, obj):
        return round(obj.average_rating, 2) if obj.rating_count > 0 else None


class ProductsBySubcategorySerializer(serializers.ModelSerializer):
    products = ProductSerializerList(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "name", "products")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ("id", "user", "rating", "text", "created_at")
        read_only_fields = ("id", "user", "rating", "text", "created_at")


class ProductDetailsSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "image", "description", "price", "full_desc", "product_image", "reviews", "average_rating")

    def get_average_rating(self, obj):
        return round(obj.average_rating, 2) if obj.rating_count > 0 else None


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "product", "amount")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items")


class CartItemAmountSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    image = serializers.ImageField(source="product.image")
    name = serializers.CharField(source="product.name")
    price = serializers.CharField(source="product.price")

    class Meta:
        model = CartItem
        fields = ("id", "product", "image", "name", "price", "amount", "total_price")


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("amount",)


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("product", "rating", "text", "created_at")
        extra_kwargs = {
            "rating": {"required": True, "min_value": 1, "max_value": 5},
            "text": {"required": False},
        }
        read_only_fields = ("created_at",)

    def validate_product(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Продукт с таким ID не существует.")
        return value

    def validate(self, data):
        user = self.context["request"].user
        product = data["product"]
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв для этого продукта.")
        return data

    def validate_text(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Текст отзыва слишком короткий. Минимум 5 символов.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
