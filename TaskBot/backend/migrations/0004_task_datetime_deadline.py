# Generated by Django 4.1.7 on 2023-03-20 23:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_telegramuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='datetime_deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 21, 2, 0, 31, 415601), verbose_name='Дэдлайн'),
        ),
    ]
