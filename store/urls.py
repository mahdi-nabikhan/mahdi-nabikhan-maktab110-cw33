from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', CartDetailViewSet, basename='order')
router.register(r'address', AddressApi, basename='address')
urlpatterns = router.urls
