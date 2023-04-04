# Generated by Django 4.1.7 on 2023-04-04 02:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_taskuser_report_file_taskuser_report_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='done_tasks_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='lost_deadline_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='datetime_deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 4, 5, 34, 13, 834652), verbose_name='Дэдлайн'),
        ),
    ]