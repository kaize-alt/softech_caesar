from http.client import HTTPResponse
from wsgiref.util import request_uri
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, filters, status

from .filters import ProductFilter
from .models import *
from .serializers import *
from ..core.serializers import LikeSerializers




class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]
    
    def get_queryset(self):
        return Category.objects.filter(parent_category__isnull=True)


class SubCategoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProductsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerList
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [JWTAuthentication,]

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return super().get_queryset()

    @extend_schema(
        parameters=[
            OpenApiParameter('category_id', type=int, description='ID категории', required=False)
        ]
    )

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        category_id = request.query_params.get("category_id")
        if category_id:
            products = self.get_queryset()
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data) 
        return Response({"detail": "Не указана категория."}, status=400)
#http://127.0.0.1:8000/api/products/by_category/?category_id=2

class ProductDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = {"name": ["icontains"]}



class CartViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        print(user)
        items = request.data.get("items", [])

        cart, _ = Cart.objects.get_or_create(user=user)
        print(cart)
        for item in items:
            product_id = item.get("product")
            print(product_id)
            amount = item.get("amount", 1)

            try:
                product = Product.objects.get(id=product_id)
                print(product)
            except Product.DoesNotExist:
                return Response({"error": f"Продукт с ID {product_id} не найден"}, status=400)

            cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
            print("Nomad")
            cart_item.amount += amount
            cart_item.save(update_fields=["amount"])

        return Response(CartSerializer(cart).data)

class CartItemViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication,]
    def destroy(self, request, *args, **kwargs):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Корзина пользователя не найдена"}, status=status.HTTP_404_NOT_FOUND)

        product_id = kwargs.get("pk")

        if not product_id:
            return Response({"error": "Поле product не указано в URL"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"success": "Товар был удален из корзины"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)


class CartItemListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CartItemAmountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

class CartItemUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        cart = self.request.user.cart
        return CartItem.objects.filter(cart__user=user, cart=cart)


class CartTotalPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cart = request.user.cart

        total_price = 0
        for item in cart.items.all():
            total_price += item.total_price

        return Response({"total_price": total_price})


class LikeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        product = request.data.get("product")
        like = Like.objects.create(user=user, product=product)
        like.is_like = True
        like.save()

        return Response(status=status.HTTP_201_CREATED)

