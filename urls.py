from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myshop.views import ProductViewSet, CartViewSet, CartItemViewSet, ReviewViewSet, OrderViewSet,OrderItemViewSet,ExampleAPIView,UserProfileView
from myshop.views import ExampleView2,SampleView
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'reviews', ReviewViewSet, basename='review') # Исправленный URL для отзывов
router.register(r"order",OrderViewSet,basename='order')
router.register(r"order-item",OrderItemViewSet,basename='order-item')
# router.register(r"order-items",OrderItemViewSet,basename='orderitems')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('example/',ExampleAPIView.as_view()),
    path('example2/',UserProfileView.as_view()),
    path('example3/',ExampleView2.as_view()),
    path('sample/',SampleView.as_view()),
    path('sample/<int:pk>/',SampleView.as_view())



]
