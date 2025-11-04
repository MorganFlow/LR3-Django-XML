from django.db import models

from django.db import models
from .utils import FIELDS

class Tour(models.Model):
    class Tour(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')
    description = models.TextField(max_length=500, verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Продолжительность (дни)')
    price = models.FloatField(verbose_name='Цена (USD)')
    difficulty = models.CharField(max_length=50, choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], verbose_name='Сложность')

    def __str__(self):
        return self.name

