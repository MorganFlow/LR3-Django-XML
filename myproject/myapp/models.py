from django.db import models

from django.db import models
from .utils import FIELDS  # Для валидации, но поля статичны

class Tour(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Уникальность для проверки дубликатов
    description = models.TextField(max_length=500)
    duration = models.IntegerField()
    price = models.FloatField()
    difficulty = models.CharField(max_length=50, choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')])

    def __str__(self):
        return self.name