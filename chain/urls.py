from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet, basename='networknode')
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
