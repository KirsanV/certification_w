from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    """
    Inline админ-панели для отображения продуктов, связанных с узлом сети
    """
    model = Product
    extra = 1
    fields = ['name', 'model', 'release_date']
    readonly_fields = ['name', 'model', 'release_date']


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления узлами сети. Просмотр, редактирование, фильтрация
    """
    list_display = [
        'name',
        'level_display',
        'city',
        'country',
        'supplier_link',
        'debt',
        'created_at'
    ]
    list_filter = ['city', 'country', 'level']
    search_fields = ['name', 'email', 'city', 'country']
    list_editable = ['debt']
    readonly_fields = ['created_at', 'level']
    inlines = [ProductInline]
    actions = ['clear_debt']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'level', 'supplier')
        }),
        ('Контактная информация', {
            'fields': ('email', 'country', 'city', 'street', 'house_number')
        }),
        ('Финансовая информация', {
            'fields': ('debt', 'created_at')
        }),
    )

    def level_display(self, obj):
        return obj.get_level_display()

    level_display.short_description = 'Уровень'

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:chain_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt=0)
        self.message_user(
            request,
            f'Задолженность очищена для {updated_count} объектов'
        )

    clear_debt.short_description = 'Очистить задолженность перед поставщиком'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления продуктами
    """
    list_display = ['name', 'model', 'release_date', 'network_node']
    list_filter = ['network_node', 'release_date']
    search_fields = ['name', 'model']
    readonly_fields = ['network_node']
