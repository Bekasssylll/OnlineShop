from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import mixins,generics
from .models import Product, Cart, CartItem, Review, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, ReviewSerializer, OrderSerializer, \
    OrderItemSerializer
from .filters import ProductFilter

"""здесь то как работает request.query_params.get("значение которое ишем",None)"""

class ExampleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        param1 = request.query_params.get('param1', None)
        if param1:
            return Response({"param1": f"param is {param1}"})
        else:
            return Response({'message': "Not have"})


"""То как работает request.user и зачем он нужен"""


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(data)



"""создаем свой класс пагинаций"""
class ProductPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000



""".auth нужен для того чтобы получить токен"""


class ExampleView2(APIView):
    def get(self, request, *args, **kwargs):
        if request.auth:
            return Response({'token': f'{request.auth}'})
        else:
            return Response({'message': "lox"})


""".authenticators для проверки прошли мы аутентификацию или нет"""
"""это по идее можно обыграть ,что то в этом стиле ,типа:"""
"""работа с request.stream"""

# class RawDataView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Чтение данных из request.stream
#         raw_data = request.stream.read()
#
#         # Обработка данных (например, если это JSON)
#         import json
#         try:
#             data = json.loads(raw_data)
#         except json.JSONDecodeError:
#             return Response({"error": "Invalid JSON"}, status=400)
#
#         # Далее можно обрабатывать данные как обычно
#         return Response(data, status=201)

"""RESPONSE и все ,что с ним связано"""
"""методы Response- .data,."""


# class DetailedResponseView(APIView):
#     def get(self, request, *args, **kwargs):
#         data = {"message": "Hello, World!"}
#         response = Response(data=data, status=status.HTTP_200_OK)
#
#         # Пример использования атрибутов
#         # response.template_name = 'example_template.html'
#         # response.render()  # Преобразует response.data в response.content
#
#         # print("Content:", response.content)
#         print("Status Code:", response.status_code)
#         # print("Accepted Renderer:", response.accepted_renderer)
#         # print("Accepted Media Type:", response.accepted_media_type)
#         # print("Renderer Context:", response.renderer_context)
#
#         return response

"""работа с миксинами и так сказать копаться в грязном белье"""
class SampleView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,*kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination
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
