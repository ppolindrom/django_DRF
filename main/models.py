from django.conf import settings
from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    """Модель курсов"""
    name = models.CharField(max_length=250, verbose_name='Наименование')
    preview = models.ImageField(upload_to='main/course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец курса',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель уроков"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    name = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='изображение урока', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео урока', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец урока',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    """Модель платежей"""

    #  варианты способа оплаты
    METHOD_CHOICES = (
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    )


    payment_date = models.DateTimeField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=25, choices=METHOD_CHOICES, verbose_name='Способ оплаты')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец платежа',
                              **NULLABLE)

    def __str__(self):
        return f'Платеж от {self.user} на сумму {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    """Модель подписки пользователя на обновления курса"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="пользователь подписки", )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
