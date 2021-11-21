from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Acc(AbstractUser):
    fio = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=20, unique=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Аккаунт'

####################################################################

RATE_CHOICES = [
    (5, '5 - Превосходно!'),
    (4, '4 - Хорошо, все понравилось.'),
    (3, '3 - Могло быть лучше.'),
    (2, '2 - Неудовлетворительно.'),
    (1, '1 - Не рекомендую.'),
]


class Reviews(models.Model):
    fio = models.ForeignKey(Acc, on_delete=models.CASCADE)
    case_number = models.CharField('Номер вашего обращения', max_length=30)
    topic = models.CharField('Тема обращения', max_length=80)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank=True)
    full_text = models.TextField('Опишите вашу тему обращения', max_length=5000)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.fio


    class Meta:
        verbose_name = 'Отзывы'