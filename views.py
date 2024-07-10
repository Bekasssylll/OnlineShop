from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Cart, CartItem, Review, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, ReviewSerializer, OrderSerializer, \
    OrderItemSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', "price"]
    ordering_fileds = ['price']
    # lookup_field = 'slug'


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Cart.objects.filter(user=self.request.user)
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.get_or_create_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id is not None:
            return Review.objects.filter(product_id=product_id)
        return Review.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



#     def create(self, request, *args, **kwargs):
#         order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
#
#         for item in request.data.get('items', []):
#             product = Product.objects.get(id=item['product_id'])
#             order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#             order_item.quantity = item.get('quantity', 1)
#             order_item.save()
#
#         order.calculate_total_amount()
#
#         serializer = self.get_serializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def update(self, request, *args, **kwargs):
#         order = self.get_object()
#
#         for item in request.data.get('items', []):
#             product = Product.objects.get(id=item['product_id'])
#             order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#             order_item.quantity = item.get('quantity', 1)
#             order_item.save()
#
#         order.calculate_total_amount()
#
#         serializer = self.get_serializer(order)
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         order = self.get_object()
#         order.is_ordered = True
#         order.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         order = serializer.save(user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""Если вам нужно, чтобы пользователь мог создавать, просматривать, обновлять и удалять как заказы,
 так и элементы заказа в одном запросе или как связанные сущности, то один ViewSet для Order может быть более удобным решением. 
 Вы можете добавить методы для работы с OrderItem внутри этого ViewSet."""


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    # def get_queryset(self):
    #     return Order.objects.filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     order_id = request.data.get('order')  # Получаем id заказа из запроса
    #     order = Order.objects.get(pk=order_id)  # Получаем объект Order по id
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid()
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     order_id = request.data.get('order')  # Получаем id заказа из запроса
    #     order = Order.objects.get(pk=order_id)  # Получаем объект Order по id
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid()
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
