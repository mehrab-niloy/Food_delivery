from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, CategoryViewSet, MenuItemViewSet, OrderViewSet

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menuitems', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Include the viewsets' URLs in the API
    path('api/', include(router.urls)),

    # Registration and login URLs
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]
