from rest_framework import serializers
from .models import Product, Cart, CartItem, Review, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # работаем с моделью Product
        fields = "__all__"  # все филдс сериализуються
        # lookup_field = 'slug'


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'content', 'rating', 'created_at')
        read_only_fields = ('id', 'created_at')  # Добавляем created_at в read_only_fields

    def create(self, validated_data):
        return Review.objects.create(
            user=validated_data['user'],
            product=validated_data['product'],
            content=validated_data['content'],
            rating=validated_data['rating']
        )

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.product = validated_data.get('product', instance.product)
        instance.content = validated_data.get('content', instance.content)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']
