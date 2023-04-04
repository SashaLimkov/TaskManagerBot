import os

from django.core.files import File

from backend.models import TelegramUser, Task, TaskUser


def create_task(user: TelegramUser, task_description: str, deadline: str, file, file_name) -> Task:
    if file:
        with open(file, "rb") as f:
            obj = Task(
                creator=user,
                task=task_description,
                datetime_deadline=deadline
            )
            obj.file.save(
                file_name,
                File(f))
            obj.save()
    else:
        obj = Task(
            creator=user,
            task=task_description,
            datetime_deadline=deadline
        )
        obj.save()
    return obj


def get_task_by_pk(task_pk: int) -> Task:
    return Task.objects.filter(pk=task_pk).prefetch_related("creator").first()


def get_created_tasks(telegram_id: int):
    return Task.objects.filter(closed_task=False, creator__telegram_id=telegram_id).all()


def get_granted_tasks(telegram_id: int):
    return list(set(TaskUser.objects.filter(task__closed_task=False, user__telegram_id=telegram_id).select_related(
        "task").all()))


def close_task_by_pk(task_pk: int):
    t = Task.objects.filter(pk=task_pk).first()
    t.closed_task = True
    t.save()


def update_task_description_db(task_pk: int, description):
    print(1111)
    t = Task.objects.filter(pk=task_pk).first()
    t.task = description
    t.save()
    print(2222)


def update_task_date_time_db(task_pk: int, date_time):
    t = Task.objects.filter(pk=task_pk).first()
    t.datetime_deadline = date_time
    t.save()


def update_task_doc_db(task_pk: int, file, file_name):
    t = Task.objects.filter(pk=task_pk).first()
    if file:
        with open(file, "rb") as f:
            t.file.save(
                file_name,
                File(f))
            t.save()
    else:
        t.file = None
        t.save()
    try:
        os.remove(file)
    except:
        pass



