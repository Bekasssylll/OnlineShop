from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_or_create_cart(cls, user):
        cart, created = cls.objects.get_or_create(user=user)
        return cart

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


"""нам нужен Order который дает нам отчеты о заказе"""
"""нам нужен OrderItem который делает соответсвенно заказы """


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_ordered = models.BooleanField(default=False)

    def total(self):
        self.total_amount = sum(item.quantity * item.product.price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order {self.id} for {self.user}"


"""статус заказа - is_ordered"""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    # def __str__(self):
    #     return f"OrderItem {self.id} for Order {self.order.id}"