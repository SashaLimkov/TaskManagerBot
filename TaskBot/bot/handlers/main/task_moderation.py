import os
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from TaskBot.settings import BASE_DIR
from backend import models
from backend.models import TaskUser
from backend.services.task import get_task_by_pk, close_task_by_pk, update_task_description_db, \
    update_task_date_time_db, update_task_doc_db
from backend.services.task_user import create_or_delete_task_user
from backend.services.telegram_user import get_profile_by_username
from bot.config.loader import bot
from bot.data import text_data as td
from bot.handlers.commands import start_command
from bot.keyboards import inline as ik
# from bot.handlers.main.task_creation import get_task_description_u, get_task_date_time_u, get_task_file_u
from bot.states.MainMenu import MainMenu
from bot.states.TaskCreation import TaskCreation
from bot.states.TaskModeration import TaskModeration
from bot.utils.date_time_worker import get_selected_datetime, is_past_date
from bot.utils.message_worker import try_edit_document_caption, dry_message_editor, send_notify
from bot.utils.validators import date_time_validator


async def moderate_task_menu_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await moderate_task_menu(message=call.message, state=state, callback_data=callback_data)


async def moderate_task_menu(message: types.Message, state: FSMContext, callback_data: dict):
    task, text, main_message_id, task_pk = await get_task_info(state=state, callback_data=callback_data)
    file = task.file.path if task.file else False
    keyboard = await ik.get_task_moderation_menu(callback_data=callback_data, task=task_pk)
    if file:
        print(type(message))
        await try_edit_document_caption(
            message=message,
            user_id=message.chat.id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state,
            file=file
        )
        return
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=message
    )


def get_users_text(users: List[TaskUser]) -> str:
    r = ""
    for index, usert in enumerate(users):
        if usert.role.name == "Исполнитель":
            r += f"{index + 1}. {'⏰❌ ' if not usert.is_not_deadline_lost else ''}{usert.user.fio} @{usert.user.username}{' выполнил' if usert.is_done else ''}\n"
        else:
            r += f"{usert.user.fio} @{usert.user.username}"
            r += "\n"
    return r


async def created_tasks_list_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    text = "Выберите задачу"
    keyboard = await ik.get_created_tasks_list(callback_data=callback_data, telegram_id=call.message.chat.id)
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=call.message
    )


async def segregate_task_moderation_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data({"task_pk": callback_data["task_pk"], "callback_data": callback_data})
    if callback_data["action_3"] == "1":
        await TaskModeration.EX_USERNAME.set()
        await enter_username(call=call, state=state)
    elif callback_data["action_3"] == "2":
        await TaskModeration.OBS_USERNAME.set()
        await enter_username(call=call, state=state)
    elif callback_data["action_3"] == "3":
        await edit_task_menu(message=call.message, state=state, callback_data=callback_data)
    else:
        await call.message.edit_reply_markup(
            reply_markup=await ik.close_task_menu(callback_data=callback_data)
        )


async def close_task(call: types.CallbackQuery, state: FSMContext):
    task_pk = int(call.data.replace("clt_", ""))
    close_task_by_pk(task_pk)
    await call.answer(text=f"Задача {task_pk} закрыта!", show_alert=True)
    await start_command(message=call.message, state=state)


async def get_task_info(state: FSMContext = {}, callback_data: dict = {}):
    data = await state.get_data()
    task_pk = callback_data.get("task_pk") or data.get("task_pk", False)
    await state.update_data({"task_pk": task_pk})
    main_message_id = data.get("main_message_id")
    task = get_task_by_pk(task_pk=task_pk)
    executors = task.executors.filter(role__name="Исполнитель").all()
    observers = task.executors.filter(role__name="Наблюдатель").all()
    text = td.TASK_MODERATION_MENU.format(
        task_pk=task_pk,
        description=task.task,
        creator_fio=task.creator.fio,
        task_deadline=task.datetime_deadline,
        creator_username=f"@{task.creator.username}",
        executors=get_users_text(executors),
        observers=get_users_text(observers),
        dd_lost_count=task.lost_deadline_count,
        percents=task.status
    )
    return (task, text, main_message_id, task_pk)


async def edit_task_menu_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await edit_task_menu(message=call.message, state=state, callback_data=callback_data)


async def edit_task_menu(message: types.message, state: FSMContext, callback_data: dict):
    task, text, main_message_id, task_pk = await get_task_info(state=state, callback_data=callback_data)
    keyboard = await ik.edit_task_menu(callback_data=callback_data)
    if task.file:
        await try_edit_document_caption(
            message=message,
            user_id=message.chat.id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state,
            file=task.file.path
        )
        return
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=message
    )


async def edit_task_segregator(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data({"task_pk": callback_data["task_pk"], "callback_data": callback_data})
    print(callback_data, "<---")
    if callback_data["action_3"] == "1":
        await TaskModeration.EX_USERNAME.set()
        await enter_username(call=call, state=state)
    elif callback_data["action_3"] == "2":
        await TaskModeration.OBS_USERNAME.set()
        await enter_username(call=call, state=state)
    elif callback_data["action_3"] == "3":
        await edit_task_menu(message=call.message, state=state, callback_data=callback_data)
    else:
        await call.message.edit_reply_markup(
            reply_markup=await ik.close_task_menu(callback_data=callback_data)
        )


async def get_ex_username(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = message.text
    user = get_profile_by_username(username=username)
    if user:
        task = get_task_by_pk(data.get("task_pk"))
        r = create_or_delete_task_user(user=user, task=task, role="Исполнитель")
        if r:
            await notify_users(task=task, user_id=user.telegram_id)
    await moderate_task_menu(message=message, state=state, callback_data=data.get("callback_data"))


async def get_obs_username(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = message.text
    user = get_profile_by_username(username=username)
    if user:
        task = get_task_by_pk(data.get("task_pk"))
        r = create_or_delete_task_user(user=user, task=task, role="Наблюдатель")
        if r:
            await notify_users(task=task, user_id=user.telegram_id)
    await moderate_task_menu(message=message, state=state, callback_data=data.get("callback_data"))


async def enter_username(call: types.CallbackQuery, state: FSMContext):
    await dry_message_editor(
        text="Введите юзернейм пользователя для добавления. Если нужно удалить пользователя, введите юзернейм повторно",
        keyboard=0,
        state=state,
        message=call.message
    )


async def task_moderation_change_task_segregator_call(call: types.CallbackQuery, state: FSMContext,
                                                      callback_data: dict):
    await task_moderation_change_task_segregator(message=call.message, state=state, callback_data=callback_data)


async def task_moderation_change_task_segregator(message: types.Message, state: FSMContext, callback_data: dict):
    await state.update_data({"callback_data": callback_data, "task_pk": callback_data["task_pk"]})
    await MainMenu.MM.set()
    if callback_data["action_3"] == "1":
        await TaskCreation.UPDATE_DESCRIPTION.set()
        await dry_message_editor(
            text="Введите описание задачи.\n"
                 "Учтите, в случае прикрепления файла к задаче, будет ограничение в 1024 символа",
            keyboard=None,
            state=state,
            message=message
        )
    elif callback_data["action_3"] == "3":
        await TaskCreation.UPDATE_FILE.set()
        await dry_message_editor(
            text="Отправьте файл, который необходимо прикрепить к задаче. либо напишите 'без файла'",
            keyboard=None,
            state=state,
            message=message
        )
    else:
        await TaskCreation.UPDATE_DATE_TIME.set()
        await dry_message_editor(
            text="Введите дату и время в формате DD.MM.YYYY HH:MM\nПример: 20.03.2023 09:45",
            keyboard=None,
            state=state,
            message=message
        )


async def update_task_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    r = await get_task_description_u(message=message, state=state)
    update_task_description_db(task_pk=data.get("task_pk"), description=r)
    await state.finish()
    await start_command(message=message, state=state)


async def update_task_date_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    r = await get_task_date_time_u(message=message, state=state)
    if r:
        update_task_date_time_db(task_pk=data.get("task_pk"), date_time=await get_selected_datetime(
            date_time=r))
    await state.finish()
    await start_command(message=message, state=state)


async def update_task_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    d = await get_task_file_u(message=message, state=state)
    if d:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = f"{message.document.file_name}"
        await bot.download_file(file_path, file_name)
        downloaded_file_path = os.path.join(BASE_DIR, file_name)
    else:
        downloaded_file_path = ""
        file_name = ""
    update_task_doc_db(task_pk=data.get("task_pk"), file=downloaded_file_path, file_name=file_name)
    await state.finish()
    await start_command(message=message, state=state)


async def get_task_file_u(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "без файла":
        await state.update_data({"file_uid": ""})
        return ""
    elif message.document:
        doc_id = message.document.file_id
        await state.update_data({"file_uid": doc_id})
        return doc_id
    await message.delete()


async def get_task_date_time_u(message: types.Message, state: FSMContext):
    date_time = message.text
    if await date_time_validator(date_time=date_time):
        if await is_past_date(date_time=date_time):
            await message.answer(text="Дата и время не может быть раньше текущего.")
        else:
            await state.update_data({"date_time": message.text})
            return message.text
    else:
        await message.answer(text="Дата и время введено в неверном формате.")
    await message.delete()


async def get_task_description_u(message: types.Message, state: FSMContext):
    await state.update_data({"task_description": message.text})
    await message.delete()
    return message.text


async def notify_users(task: models.Task, user_id: int, report_text="", report_file=""):
    if report_text:
        text = report_text
    else:
        text = "Новая задача!\n" + pretty_task_info(task=task)
    if report_file:
        file = report_file
    else:
        file = task.file.path if task.file else None
    keyboard = await ik.back_to_mm()
    await send_notify(
        file=file,
        text=text,
        keyboard=keyboard,
        user_id=user_id
    )


def pretty_task_info(task: models.Task):
    executors = task.executors.filter(role__name="Исполнитель").all()
    observers = task.executors.filter(role__name="Наблюдатель").all()
    text = td.TASK_INFO_MENU.format(
        task_pk=task.pk,
        description=task.task,
        creator_fio=task.creator.fio,
        task_deadline=task.datetime_deadline,
        creator_username=f"@{task.creator.username}",
        executors=get_users_text(executors),
        observers=get_users_text(observers),
        dd_lost_count=task.lost_deadline_count,
        percents=task.status
    )
    return text
