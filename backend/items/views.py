from http.client import HTTPResponse
from wsgiref.util import request_uri

from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, filters, status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Case, When, FloatField


from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters


from .filters import ProductFilter
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

from ..core.serializers import LikeSerializers


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]


class SubCategoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProductsBySubcategoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = ProductsBySubcategorySerializer

    def retrieve(self, request, *args, **kwargs):
        subcategory = self.get_object()
        products = subcategory.products.all()  # Получение продуктов, связанных с подкатегорией
        ordering = self.request.query_params.get('ordering')

        if ordering in ['price', '-price', 'created_at', '-created_at']:
            products = products.order_by(ordering)

        serializer = self.get_serializer(subcategory)
        data = serializer.data
        data['products'] = ProductSerializerList(products, many=True).data
        return Response(data)



class ProductSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.prefetch_related('product_image', 'reviews__user').all()
    serializer_class = ProductSearchSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ProductFilter
    search_fields = {"name": ["icontains"]}
    ordering_fields = ['price', 'created_at']  # Поля для сортировки
    ordering = ['-created_at']

class ProductDetailsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer


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


class CardItemListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
    
class ReviewCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Автоматически добавляем пользователя в данные"""
        serializer.save(user=self.request.user)
