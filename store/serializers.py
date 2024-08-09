from rest_framework import serializers
from .models import *
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    # def __init__(self, *args, **kwargs):
    #     files = kwargs.pop('files')
    #
    #     super().__init__(*args, **kwargs)
    #     if files:
    #         images_file_dict = {
    #             field: serializers.ImageField(required=False, write_only=True)
    #             for field in files
    #         }
    #         self.fields.update(**images_file_dict)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance).data
        print(rep['category'])
        return rep

    def create(self, validated_data):
        # validated_data_copy = validated_data.copy()
        # validated_files = []
        # for key, value in validated_data_copy.items():
        #     if isinstance(value, (TemporaryUploadedFile, InMemoryUploadedFile)):
        #         validated_files.append(value)
        #         validated_data.pop(key)
        images = validated_data.pop('images')
        colors = validated_data.pop('color_value')
        sizes = validated_data.pop('size_value')
        owner = self.context['request'].user
        products = Product.objects.create(owner=owner, **validated_data)

        # for image in validated_files:
        #     ProductImage.objects.create(image=image, product=products, )
        for image in images:
            ProductImage.objects.create(product=products, **image)
        for color in colors:
            products.color_value.add(color)

        for size in sizes:
            products.size_value.add(size)
        return products


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'is_paid']

    def create(self, validated_data):
        cart_owner = self.context['request'].user
        customer = Customer.objects.get(id=cart_owner.id)
        is_paid = validated_data['is_paid']

        return Cart.objects.create(cart_owner=customer, is_paid=is_paid)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'point', 'quantity', 'cart']
        read_only_fields = ['cart']

    def create(self, validated_data):
        cart_owner = self.context['request'].user
        customer = Customer.objects.get(id=cart_owner.id)
        carts = Cart.objects.filter(cart_owner=customer, is_paid=False).first()
        point = validated_data['point']
        quantity = validated_data['quantity']
        product = validated_data['product']
        if not carts:
            carts = Cart.objects.create(cart_owner=customer, is_paid=False)
        return OrderDetail.objects.create(cart=carts, point=point, quantity=quantity, product=product)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        address_owner = self.context['request'].user
        customer = Customer.objects.get(id=address_owner.id)
        return Address.objects.create(user=customer, **validated_data)
