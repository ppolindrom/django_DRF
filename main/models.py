from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    """Модель курсов"""
    course_name = models.CharField(max_length=250, verbose_name='Наименование')
    course_preview = models.ImageField(upload_to='main/course/', verbose_name='Превью', **NULLABLE)
    course_description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель уроков"""
    lesson_name = models.CharField(max_length=250, verbose_name='Наименование')
    lesson_description = models.TextField(verbose_name='Описание')
    lesson_preview = models.ImageField(upload_to='main/lesson/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
