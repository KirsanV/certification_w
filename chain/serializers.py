from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Обеспечивает сериализацию данных о продуктах
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date', 'network_node']
        read_only_fields = ['id']


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Включает связанные продукты, информацию о поставщике и читаемое
    представление уровня узла
    """
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'level', 'level_display', 'email',
            'country', 'city', 'street', 'house_number',
            'supplier', 'supplier_name', 'debt', 'created_at', 'products'
        ]
        read_only_fields = ['debt', 'created_at', 'level_display']


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новых узлов сети
    """
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'email', 'country', 'city',
            'street', 'house_number', 'supplier'
        ]


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления существующих узлов сети
    """
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'email', 'country', 'city',
            'street', 'house_number', 'supplier'
        ]
        read_only_fields = ['debt']
