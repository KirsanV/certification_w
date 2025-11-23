from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """Модель узла сети по продаже электроники"""

    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Уровень иерархии')

    email = models.EmailField(
        verbose_name='Email',
        validators=[EmailValidator()]
    )
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Поставщик'
    )

    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.00,
        verbose_name='Задолженность перед поставщиком'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Узел сети'
        verbose_name_plural = 'Узлы сети'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['city']),
            models.Index(fields=['country']),
            models.Index(fields=['supplier']),
        ]

    def save(self, *args, **kwargs):
        """Автоматически определяем уровень иерархии на основе поставщика"""
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_level_display()}: {self.name} ({self.city})"


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Узел сети'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['release_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.model})"
