# Generated by Django 3.2.5 on 2021-11-12 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_reviews_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(5, '5 - Превосходно!'), (4, '4 - Хорошо, все понравилось.'), (3, '3 - Могло быть лучше.'), (2, '2 - Неудовлетворительно.'), (1, '1 - Не рекомендую.')]),
        ),
    ]