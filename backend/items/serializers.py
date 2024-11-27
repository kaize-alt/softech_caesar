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
    subcategories = SubCategorySerializerList(many=True)
    class Meta:
        model = Category
        fields = ("id", "subcategories")


class ProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "image")


class ProductSerializer(serializers.ModelSerializer):
    products = ProductSerializerList(many=True)

    class Meta:
        model = Category
        fields = ("id", "products")

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("image", )


class ProductDetailsSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ("name", "image", "description", "price", "product_image")


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "product", "amount")



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,)
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
        fields = ("product", "amount",)

class CartTotalPriceSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
