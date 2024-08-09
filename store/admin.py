from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ('username', 'points')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'title')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_owner',)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('cart', 'quantity', 'product')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'zip_code')
