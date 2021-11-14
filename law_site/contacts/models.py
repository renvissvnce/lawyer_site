from django.db import models
from datetime import datetime

class Feedback(models.Model):
    fio = models.CharField('Ваше ФИО', max_length=35)
    phone = models.CharField('Ваш телефон', max_length=25)
    mail = models.CharField('Ваша электронная почта', max_length=30)
    topic = models.CharField('Тема обращения', max_length=80)
    full_text = models.TextField('Опишите вашу тему обращения', max_length=5000)
    date = models.DateTimeField(default=datetime.utcnow(), blank=True)


    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Обратная свзяь'
# Create your models here.
