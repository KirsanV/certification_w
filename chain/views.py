from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import NetworkNode, Product
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateSerializer,
    NetworkNodeUpdateSerializer,
    ProductSerializer
)


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение только для активных сотрудников
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для узлов сети с CRUD операциями
    """
    queryset = NetworkNode.objects.select_related('supplier').prefetch_related('products')
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['country', 'city', 'level']
    search_fields = ['name', 'city', 'country', 'email']
    ordering_fields = ['name', 'created_at', 'debt']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return NetworkNodeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NetworkNodeUpdateSerializer
        return NetworkNodeSerializer

    def perform_create(self, serializer):
        """Автоматически устанавливаем уровень при создании"""
        instance = serializer.save()

    @action(detail=False, methods=['get'])
    def factories(self, request):
        """Получить только заводы (уровень 0)"""
        factories = self.queryset.filter(level=0)
        serializer = self.get_serializer(factories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Расширенный поиск"""
        query = request.query_params.get('q', '')
        if query:
            nodes = self.queryset.filter(
                Q(name__icontains=query)
                | Q(city__icontains=query)
                | Q(country__icontains=query)
                | Q(email__icontains=query)
            )
            serializer = self.get_serializer(nodes, many=True)
            return Response(serializer.data)
        return Response([])


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для продуктов
    """
    queryset = Product.objects.select_related('network_node')
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['network_node', 'release_date']
    search_fields = ['name', 'model']
    ordering_fields = ['name', 'release_date']
    ordering = ['name']
