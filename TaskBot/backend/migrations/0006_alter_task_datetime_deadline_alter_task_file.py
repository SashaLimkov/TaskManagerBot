# Generated by Django 4.1.7 on 2023-04-03 23:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_task_closed_task_alter_task_datetime_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='datetime_deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 4, 2, 7, 30, 459214), verbose_name='Дэдлайн'),
        ),
        migrations.AlterField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files', verbose_name='Файл'),
        ),
    ]