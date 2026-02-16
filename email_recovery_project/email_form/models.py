from django.db import models
from django.utils import timezone
import random
import string

class EmailRequest(models.Model):
    ACTION_CHOICES = [
        ('create', 'Создание'),
        ('recovery', 'Восстановление'),
        ('block', 'Блокировка'),
    ]
    
    # Номер заявки
    request_number = models.CharField(max_length=20, unique=True, verbose_name='Номер заявки')
    
    # Действие
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Действие')
    reason = models.TextField(blank=True, null=True, verbose_name='Причина')
    
    # Организация
    authority = models.CharField(
        max_length=100, 
        default='Департамент здравоохранения города Москвы',
        verbose_name='Орган исполнительной власти или учреждение'
    )
    institution = models.CharField(
        max_length=100,
        default='ГБУЗ ГКБ № 29 им. Н.Э. Баумана',
        verbose_name='Подведомственное учреждение'
    )
    
    # Персональные данные
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    department = models.CharField(max_length=200, verbose_name='Отдел')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    
    # Адрес
    address = models.CharField(
        max_length=200,
        default='г. Москва, Госпитальная площадь, 2',
        verbose_name='Адрес'
    )
    building = models.CharField(max_length=10, verbose_name='Корпус')
    office = models.CharField(max_length=50, verbose_name='Кабинет')
    
    # Для восстановления/блокировки
    current_email = models.EmailField(blank=True, null=True, verbose_name='Текущая электронная почта')
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено на почту')
    
    class Meta:
        verbose_name = 'Заявка на email'
        verbose_name_plural = 'Заявки на email'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка №{self.request_number} - {self.get_action_display()}"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            # Генерация номера заявки: GKB29-YYYYMMDD-XXXX
            date_str = timezone.now().strftime('%d%m%Y')
            random_str = ''.join(random.choices(string.digits, k=4))
            self.request_number = f"GKB29-{date_str}-{random_str}"
        super().save(*args, **kwargs)