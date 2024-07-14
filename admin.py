from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Cart, CartItem, Review, Order, OrderItem



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'created_at','updated_at','image']
    list_filter = ['created_at', 'updated_at', 'price']
    search_fields = ['name', 'description']
    list_editable = ['price']
    ordering = ['name']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return '-'

    image_tag.short_description = 'Image'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username']
    ordering = ['user']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'quantity']
    search_fields = ['cart__user__username', 'product__name']
    ordering = ['cart', 'product']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']
    ordering = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'is_ordered']
    list_filter = ['is_ordered']
    search_fields = ['user__username']
    ordering = ['user']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order__user__username', 'product__name']
    ordering = ['order', 'product']
