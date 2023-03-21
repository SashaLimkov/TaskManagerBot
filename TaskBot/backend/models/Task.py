import datetime

from backend.models import TelegramUser
from backend.models.TimeBasedModel import TimeBasedModel
from django.db import models


class Task(TimeBasedModel):
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="created_tasks", blank=True)
    task = models.TextField("Поставленная задача", max_length=4096, blank=True)
    file = models.FileField("Файл", upload_to="files", blank=True, null=True)
    datetime_deadline = models.DateTimeField("Дэдлайн", blank=True, default=datetime.datetime.now())
    status = models.FloatField("Процент выполнения", default=0)
    is_done = models.BooleanField("Все выполнили", default=False)
    lost_deadline_count = models.IntegerField("Просрочившие исполнители", default=0)
    closed_task = models.BooleanField("Закрытая задача", default=False)

    def __str__(self):
        return self.task[:32] + "..."

    @property
    def pretty_info(self):
        return self.__str__()
