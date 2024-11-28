from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name",)


class SubCategorySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "image",)


class SubCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializerList(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ("id", "subcategories",)


class ProductSerializerList(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = Product
        fields = ("id", "name", "image", "price", "category_name",)



class ProductSerializer(serializers.ModelSerializer):
    products = ProductSerializerList(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "products")

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("image", )


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "image", "description", "price")



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "product", "amount",)



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ("id", "items")


class CartItemAmountSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    image = serializers.ImageField(source="product.image", read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "image", "name", "price", "amount", "total_price",)

    def get_total_price(self, obj):
        return obj.amount * obj.product.price



class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("product", "amount",)
    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0.")
        return value

class CartTotalPriceSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
