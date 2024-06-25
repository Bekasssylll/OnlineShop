from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myshop.views import ProductViewSet, CartViewSet, CartItemViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'reviews', ReviewViewSet, basename='review')  # Исправленный URL для отзывов

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
