import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from TaskBot.settings import BASE_DIR
from backend.services.task import get_task_by_pk
from backend.services.task_user import update_task_report, get_user_task
from backend.services.telegram_user import get_profile_by_telegram_id, get_profile_by_pk
from bot.config.loader import bot
from bot.handlers.main.task_moderation import pretty_task_info, notify_users
from bot.keyboards import inline as ik
from bot.data import text_data as td
from bot.states.FillReport import FillReportState
from bot.utils.message_worker import try_edit_document_caption, dry_message_editor


async def granted_task_menu_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await granted_task_menu(message=call.message, state=state, callback_data=callback_data)


async def granted_task_menu(message: types.Message, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    task_pk = callback_data["task_pk"]
    task = get_task_by_pk(task_pk=task_pk)
    file = task.file.path if task.file else False
    user = get_profile_by_telegram_id(message.chat.id)
    user_task = get_user_task(user=user, task=task)
    role = user_task.role.name
    keyboard = await ik.granted_task_menu(callback_data=callback_data, done=user_task.is_done,
                                          executor=False if role != "Исполнитель" else True)
    text = pretty_task_info(task=task)
    if file:
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


async def granted_tasks_list_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    text = "Выберите задачу"
    keyboard = await ik.get_granted_tasks_list(callback_data=callback_data, telegram_id=call.message.chat.id)
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=call.message
    )


async def report_menu_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await report_menu(message=call.message, state=state, callback_data=callback_data)


async def report_menu(message: types.Message, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    await FillReportState.MENU.set()
    main_message_id = data.get("main_message_id", False)
    report_text = data.get("report_text", "")
    file_uid = data.get("report_file_uid", "")
    text = td.REPORT.format(report_text=report_text)
    keyboard = await ik.report_fill_menu(callback_data=callback_data, any_of_fields=any((text, file_uid)))
    if file_uid:
        await try_edit_document_caption(
            message=message,
            user_id=message.chat.id,
            text=text,
            main_message_id=main_message_id,
            keyboard=keyboard,
            state=state,
            file=None,
            report=True
        )
    else:
        await dry_message_editor(
            text=text,
            keyboard=keyboard,
            state=state,
            message=message
        )


async def report_menu_segregate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(callback_data=callback_data)
    if callback_data["action_4"] == "1":
        await FillReportState.TEXT.set()
        await dry_message_editor(
            text="Заполните текст отчета",
            keyboard=await ik.back_to_granted_task_report_menu(callback_data=callback_data),
            state=state,
            message=call.message
        )
    elif callback_data["action_4"] == "2":
        await FillReportState.FIlE.set()
        await dry_message_editor(
            text="Загрузите файл или напишите 'без файла'",
            keyboard=await ik.back_to_granted_task_report_menu(callback_data=callback_data),
            state=state,
            message=call.message
        )
    else:
        await call.answer(text=f"Поздравляем, вы завершили выполнение задачи {callback_data['task_pk']}",
                          show_alert=True)
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
        data = await state.get_data()
        report_text = data.get("report_text", "")
        task_pk = callback_data["task_pk"]
        task = get_task_by_pk(task_pk=task_pk)
        user = get_profile_by_telegram_id(telegram_id=call.message.chat.id)
        report = await report_saving(
            user=user,
            task=task,
            report_text=report_text,
            report_file=downloaded_file_path,
            report_file_name=file_name
        )
        rt = f"Отчет от {user.fio} @{user.username}!\nЗадача №{task_pk}.\n\n"
        rt += report_text
        await notify_users(task=task, user_id=task.creator.telegram_id, report_text=rt,
                           report_file=report.report_file.path if report.report_file else None)
        await granted_tasks_list_menu(
            call=call,
            state=state,
            callback_data=callback_data
        )


async def get_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(report_text=text)
    data = await state.get_data()
    await message.delete()
    await report_menu(
        message=message,
        state=state,
        callback_data=data.get("callback_data", {})
    )


async def get_report_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await get_report_file_u(message=message, state=state)
    await message.delete()
    await report_menu(message=message, state=state, callback_data=data.get("callback_data", {}))


async def get_report_file_u(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "без файла":
        await state.update_data({"report_file_uid": ""})
        return ""
    elif message.document:
        doc_id = message.document.file_id
        await state.update_data({"report_file_uid": doc_id})
        return doc_id
    await message.delete()


async def report_saving(user, task, report_text, report_file, report_file_name):
    return update_task_report(
        user=user,
        task=task,
        report_file=report_file,
        report_text=report_text,
        report_file_name=report_file_name
    )


async def show_executors_list(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    task = get_task_by_pk(callback_data["task_pk"])
    await dry_message_editor(
        text="Выберите пользователя",
        keyboard=await ik.executors_list(task=task, callback_data=callback_data),
        state=state,
        message=call.message
    )


async def show_executor_profile(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user = get_profile_by_pk(user_pk=callback_data["user_pk"])
    print(user.username)
    keyboard = await ik.back_to_executors_list(callback_data=callback_data)
    await show_profile(
        message=call.message,
        user=user,
        keyboard=keyboard,
        state=state
    )


async def show_profile(message: types.Message, state: FSMContext, user=None, keyboard=None):
    if not user:
        user = get_profile_by_telegram_id(telegram_id=message.chat.id)
    text = td.PROFILE.format(
        fio=user.fio,
        username=user.username,
        phone=user.phone_number,
        done_count=user.done_tasks_count,
        lost_count=user.lost_deadline_count,
    )
    if not keyboard:
        keyboard = await ik.back_to_mm()
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=message
    )
