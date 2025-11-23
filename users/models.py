from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    Добавляет дополнительные поля для управления доступом сотрудников к системе
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активный сотрудник'),
        help_text=_('Определяет, имеет ли пользователь доступ к API')
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
