import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from TaskBot.settings import BASE_DIR
from backend.services.task import create_task
from backend.services.telegram_user import get_profile_by_telegram_id
from bot.config.loader import bot
from bot.data import text_data as td
from bot.handlers.main.task_moderation import moderate_task_menu
from bot.keyboards import inline as ik
from bot.states.TaskCreation import TaskCreation
from bot.utils.date_time_worker import is_past_date, get_selected_datetime
from bot.utils.message_worker import dry_message_editor, try_edit_document_caption
from bot.utils.validators import date_time_validator


async def call_create_task_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    print(123)
    await create_task_menu(message=call.message, state=state, callback_data=callback_data)


async def create_task_menu(message: types.message, state: FSMContext, callback_data: dict):
    print("___" * 10)
    await TaskCreation.MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    task_number = "Сформируется автоматически"
    task_description = data.get("task_description", "")
    date_time = data.get("date_time", "")
    doc_uid = data.get("file_uid", False)
    print(doc_uid)
    text = td.TASK_CREATION_MENU.format(
        task_number=task_number,
        task_description=task_description,
        date_time=date_time
    )
    keyboard = await ik.get_create_task_menu(
        callback_data=callback_data,
        done=all((task_description, date_time))
    )
    if doc_uid:
        await try_edit_document_caption(
            message=message,
            user_id=message.chat.id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state
        )
        return
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=message
    )


async def task_create_segregation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data({"callback_data": callback_data})
    if callback_data["action_3"] == "1":
        await TaskCreation.DESCRIPTION.set()
        await dry_message_editor(
            text="Введите описание задачи.\n"
                 "Учтите, в случае прикрепления файла к задаче, будет ограничение в 1024 символа",
            keyboard=None,
            state=state,
            message=call.message
        )
    elif callback_data["action_3"] == "2":
        await TaskCreation.FILE.set()
        await dry_message_editor(
            text="Отправьте файл, который необходимо прикрепить к задаче. либо напишите 'без файла'",
            keyboard=None,
            state=state,
            message=call.message
        )
    elif callback_data["action_3"] == "3":
        await TaskCreation.DATE_TIME.set()
        await dry_message_editor(
            text="Введите дату и время в формате DD.MM.YYYY HH:MM\nПример: 20.03.2023 09:45",
            keyboard=None,
            state=state,
            message=call.message
        )
    else:
        await TaskCreation.MENU.set()
        data = await state.get_data()
        task_description = data.get("task_description", "")
        date_time = data.get("date_time", "")
        if call.message.document:
            file_id = call.message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            file_name = f"{call.message.document.file_name}"
            await bot.download_file(file_path, file_name)
            downloaded_file_path = os.path.join(BASE_DIR, file_name)
        else:
            downloaded_file_path = ""
            file_name = ""
        user = get_profile_by_telegram_id(telegram_id=call.message.chat.id)
        task = create_task(
            user=user,
            task_description=task_description,
            deadline=await get_selected_datetime(
                date_time=date_time
            ),
            file=downloaded_file_path,
            file_name=file_name
        )
        await call.answer(text=f"Задача №{task.pk} сформирована.", show_alert=True)
        await state.update_data({"task_pk": task.pk})
        await moderate_task_menu(
            message=call.message,
            state=state,
            callback_data=callback_data
        )


async def get_task_description_u(message: types.Message, state: FSMContext):
    await state.update_data({"task_description": message.text})
    await message.delete()
    return message.text


async def get_task_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await get_task_description_u(message=message, state=state)
    await create_task_menu(message=message, state=state, callback_data=data.get("callback_data", False))


async def get_task_file_u(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "без файла":
        await state.update_data({"file_uid": ""})
        return ""
    elif message.document:
        doc_id = message.document.file_id
        await state.update_data({"file_uid": doc_id})
        return doc_id
    await message.delete()


async def get_task_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await get_task_file_u(message=message, state=state)
    await create_task_menu(message=message, state=state, callback_data=data.get("callback_data", False))


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


async def get_task_date_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await get_task_date_time_u(message=message, state=state)
    await create_task_menu(message=message, state=state, callback_data=data.get("callback_data", False))


