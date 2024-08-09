from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Customer(User):
    points = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Customer'
        verbose_name = 'Customer'


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    color_value = models.ManyToManyField(Color, related_name='color_value')
    size_value = models.ManyToManyField(Size, related_name='size_value')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    discount = models.FloatField(null=True)
    product_point = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_owner')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_owner.username

    def save(self, *args, **kwargs):
        pass



class OrderDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_in_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_in_order')
    quantity = models.IntegerField()
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.point += (self.quantity * self.product.product_point)
        super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
