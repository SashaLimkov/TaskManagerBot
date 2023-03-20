from django.db import models

from backend.models.Role import Role
from backend.models.TimeBasedModel import TimeBasedModel


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    fio = models.CharField("ФИО пользователя", max_length=255)
    username = models.CharField("Никнейм пользователя", max_length=255)
    telegram_id = models.BigIntegerField("Телеграм ID", unique=True)
    phone_number = models.CharField("Контактный номер", max_length=30, blank=True)

    def __str__(self):
        return self.fio
