from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import *
from store.serializers import ProductSerializer, CartSerializer, OrderSerializer, AddressSerializer


# Create your views here.origin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, files=list(request.FILES.keys()))

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(cart_owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartDetailViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OrderDetail.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(id=user.id)
        print(type(customer))
        cart = Cart.objects.get(cart_owner=customer, is_paid=False)
        queryset = self.queryset.filter(cart=cart)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddressApi(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        user = self.request.user
        customer = Customer.objects.get(id=user.id)
        queryset = self.queryset.filter(user=customer)
        return queryset
