# Generated by Django 4.1.7 on 2023-03-20 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_task_photo_task_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, verbose_name='Контактный номер'),
        ),
    ]
