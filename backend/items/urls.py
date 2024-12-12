from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import *

items_router = routers.DefaultRouter()

items_router.register(r"Category", CategoryViewSet, basename="category")
items_router.register(r"sub_category", SubCategoryViewSet, basename="sub_category")
items_router.register(r"products_by_subcategory", ProductsBySubcategoryViewSet, basename="products_by_subcategory")
items_router.register(r"product_search", ProductSearchViewSet, basename="product_search")
items_router.register(r"product_details", ProductDetailsViewSet, basename="product_details")
items_router.register(r"cart", CartViewSet, basename="cart")
items_router.register(r"item_delete", CartItemViewSet, basename="item_delete")
items_router.register(r"cart_list", CardItemListViewSet, basename="cart_list")
items_router.register(r"cart_item_update", CartItemUpdateViewSet, basename="cart_item_update")
items_router.register(r"cart_total_price", CartTotalPriceViewSet, basename="cart_total_price")
items_router.register(r"like", LikeViewSet, basename="like")
items_router.register(r"review_create", ReviewCreateViewSet, basename="review")
