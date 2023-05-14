import asyncio
import datetime

from django.db import models
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from backend.models import TelegramUser
from backend.models.TimeBasedModel import TimeBasedModel
from bot.config.loader import bot


class Task(TimeBasedModel):
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="created_tasks", blank=True)
    task = models.TextField("Поставленная задача", max_length=4096, blank=True)
    file = models.FileField("Файл", upload_to="files", blank=True, null=True)
    datetime_deadline = models.DateTimeField("Дэдлайн", blank=True)
    status = models.FloatField("Процент выполнения", default=0)
    is_done = models.BooleanField("Все выполнили", default=False)
    lost_deadline_count = models.IntegerField("Просрочившие исполнители", default=0)
    closed_task = models.BooleanField("Закрытая задача", default=False)
    previous_file = None
    previous_task = None
    previous_datetime = None
    def __str__(self):
        return self.task[:32] + "..."

    @property
    def pretty_info(self):
        return self.__str__()


async def notify_executors_task(telegram_users: list, text):
    for telegram_id in telegram_users:
        await bot.send_message(
            chat_id=telegram_id,
            text=text
        )


@receiver(post_init, sender=Task, dispatch_uid="update_prev_fields")
def update_prev(sender, instance, **kwargs):
    instance.previous_file = instance.file
    instance.previous_task = instance.task
    instance.previous_datetime = instance.datetime_deadline

@receiver(post_save, sender=Task, dispatch_uid="notify executors")
def notify_executors(sender, instance, created, **kwargs):
    task = instance
    print(instance.previous_file != instance.file, instance.previous_task != instance.task, instance.previous_datetime != instance.datetime_deadline)
    if instance.previous_file != instance.file or instance.previous_task != instance.task or instance.previous_datetime != instance.datetime_deadline or created:
        executors = task.executors.filter(role__name="Исполнитель").all()
        text = f"Задача №{task.pk} {task.__str__()} была обновлена."
        executors_id_list = [executor.user.telegram_id for executor in executors]
        asyncio.run(notify_executors_task(telegram_users=executors_id_list, text=text))
        print("NOTIFY DONE")

