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
        items = request.data.get("items", [])

        cart, _ = Cart.objects.get_or_create(user=user)

        for item in items:
            product_id = item.get("product")
            amount = item.get("amount", 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Продукт с ID {product_id} не найден"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.amount += amount
                cart_item.save()
            else:
                cart_item.amount = amount
                cart_item.save()

      
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

class CartItemListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class CartItemUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

class CartTotalPriceViewSet(viewsets.ViewSet):
    serializer_class = CartTotalPriceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        cart = Cart.objects.get(user=request.user)
        total_price = sum(item.product.price * item.amount for item in cart.cartitem_set.all())
        return Response({"total_price": total_price})

class LikeViewSet(viewsets.ViewSet):
    serializer_class = LikeSerializers
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        product_id = request.data.get("product_id")
        is_like = request.data.get("is_like", True)  
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, product=product)
        like.is_like = is_like
        like.save()

        return Response({"message": "Статус лайка обновлен"})
