from backend.models import TimeBasedModel, TelegramUser, Task, Role
from django.db import models
import decimal
from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class TaskUser(TimeBasedModel):
    class Meta:
        verbose_name = "Ответственный за задачу"
        verbose_name_plural = "Ответственные за задачи"

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="user_tasks")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="executors")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="user_task_role", to_field="name",
                             default="Исполнитель")
    is_done = models.BooleanField("Задача выполнена", default=False)
    is_not_deadline_lost = models.BooleanField("Задача не просрочена", default=True)

    def __str__(self):
        return f"{self.user.fio} -> {self.task.pretty_info}"


@receiver(post_save, sender=TaskUser, dispatch_uid="update task statistics")
def update_task_statistics(sender, instance, **kwargs):
    task = instance.task

    lost_deadline_count = task.executors.filter(is_not_deadline_lost=False, role__name="Исполнитель").count()
    task.lost_deadline_count = lost_deadline_count

    executors_count = task.executors.filter(role__name="Исполнитель").count()
    executor_tasks_done_count = task.executors.filter(is_done=True, role__name="Исполнитель").count()
    if executor_tasks_done_count != executors_count:
        decimal.getcontext().prec = 2
        task.status = float(Decimal(Decimal(executor_tasks_done_count) / Decimal(executors_count)) * Decimal(100))
        task.is_done = False
    else:
        task.status = 100
        task.is_done = True
    task.save()


@receiver(post_delete, sender=TaskUser, dispatch_uid="update task statistics delete")
def update_task_statistics_delete(sender, instance, **kwargs):
    update_task_statistics(sender, instance, **kwargs)
