import datetime

from backend.models import Task
from backend.services.task_user import get_user_task
from bot.config.loader import bot
from bot.handlers.main.task_moderation import get_users_text
from bot.data import text_data as td


async def notifier():
    tasks = Task.objects.filter(closed_task=False).all()
    for task in tasks:
        if datetime.date.today() >= task.datetime_deadline.date():
            executors = task.executors.filter(is_done=False).all()
            observers = task.executors.filter(role__name="Наблюдатель").all()
            text = td.TASK_INFO_MENU.format(
                task_pk=task.pk,
                description=task.task,
                creator_fio=task.creator.fio,
                task_deadline="<b>Сегодня</b>" if datetime.date.today() == task.datetime_deadline.date() else "<b>Просрочен</b>",
                creator_username=f"@{task.creator.username}",
                executors=get_users_text(executors),
                observers=get_users_text(observers),
                dd_lost_count=task.lost_deadline_count,
                percents=task.status
            )
            for executor in executors:
                await bot.send_message(chat_id=executor.user.telegram_id, text=text)


async def update_deadline():
    tasks = Task.objects.filter(closed_task=False).all()
    for task in tasks:
        executors = task.executors.filter(is_done=False, is_not_deadline_lost=True).all()
        if datetime.datetime.now().time() > task.datetime_deadline.time() and datetime.date.today() >= task.datetime_deadline.date():
            observers = task.executors.filter(role__name="Наблюдатель").all()
            text = "Дэдлайн просрочен.\n" + td.TASK_INFO_MENU.format(
                task_pk=task.pk,
                description=task.task,
                creator_fio=task.creator.fio,
                task_deadline="<b>Сегодня</b>" if datetime.date.today() == task.datetime_deadline.date() else "<b>Просрочен</b>",
                creator_username=f"@{task.creator.username}",
                executors=get_users_text(executors),
                observers=get_users_text(observers),
                dd_lost_count=task.lost_deadline_count,
                percents=task.status
            )
            for executor in executors:
                task_user = get_user_task(task=task, user=executor.user)
                task_user.is_not_deadline_lost = False
                user = task_user.user
                user.lost_deadline_count += 1
                user.save()
                task_user.save()
                await bot.send_message(chat_id=executor.user.telegram_id, text=text)
                await bot.send_message(
                    text=f"{executor.user.fio} просрочил задание\n"+text,
                    chat_id=task.creator.telegram_id
                )
