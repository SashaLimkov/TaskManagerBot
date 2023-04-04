import os

from backend.models import TelegramUser, Task, TaskUser, Role
from django.core.files import File


def get_user_task(user, task):
    return TaskUser.objects.filter(task=task, user=user).select_related("user").first()

def create_or_delete_task_user(user: TelegramUser, task: Task, role):
    r = TaskUser.objects.filter(task=task, user=user).first()
    if r:
        r.delete()
    else:
        ro = Role.objects.filter(name=role).first()
        TaskUser.objects.create(
            user=user,
            task=task,
            role=ro
        )
        return True


def update_task_report(user: TelegramUser, task: Task, report_text: str = "", report_file: str = "",
                       report_file_name: str = ""):
    user.done_tasks_count += 1
    user.save()
    r = TaskUser.objects.filter(task=task, user=user).first()
    if report_text:
        r.report_text = report_text
    if report_file:
        with open(report_file, "rb") as f:
            r.report_file.save(
                report_file_name,
                File(f))
    r.is_done = True
    r.save()
    try:
        os.remove(report_file)
    except:
        pass
    return r


def create_role(name: str):
    return Role.objects.create(name=name)
