from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.services.task import get_task_by_pk
from bot.data import text_data as td
from bot.handlers.main.granted_tasks import granted_tasks_list_menu
from bot.handlers.main.task_creation import create_task_menu
from bot.handlers.main.task_moderation import created_tasks_list_menu, pretty_task_info
from bot.keyboards import inline as ik
from bot.states.MainMenu import MainMenu
from bot.utils.message_worker import dry_message_editor


async def get_task_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await dry_message_editor(
        text=td.TASKS_MENU,
        keyboard=await ik.get_main_tasks_menu(callback_data=callback_data),
        state=state,
        message=call.message
    )


async def tasks_menu_segregation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await MainMenu.MM.set()
    if callback_data["action_2"] == "1":
        await create_task_menu(message=call.message, state=state, callback_data=callback_data)
    elif callback_data["action_2"] == "2":
        await created_tasks_list_menu(call=call, state=state, callback_data=callback_data)
    elif callback_data["action_2"] == "3":
        await granted_tasks_list_menu(call=call, state=state, callback_data=callback_data)
    else:
        await find_task_menu_call(call=call, state=state, callback_data=callback_data)


async def find_task_menu_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await find_task_menu(message=call.message, state=state, callback_data=callback_data)


async def find_task_menu(message: types.Message, state: FSMContext, callback_data: dict):
    await state.update_data(callback_data=callback_data)
    await MainMenu.FIND.set()
    await dry_message_editor(
        text="Введите номер задачи",
        keyboard=await ik.back_to_tasks_menu(callback_data=callback_data),
        state=state,
        message=message
    )


async def find_task(message: types.Message, state: FSMContext):
    task_pk = message.text
    data = await state.get_data()
    callback_data = data.get("callback_data", {})
    task = get_task_by_pk(task_pk=task_pk)
    if not task:
        await message.answer(f'Задача {task_pk} не найдена.')
        await message.delete()
        await find_task_menu(message=message, state=state, callback_data=callback_data)
    await message.delete()
    text = pretty_task_info(task=task)
    keyboard = await ik.back_to_find_tasks_menu(callback_data=callback_data)
    await dry_message_editor(
        text=text,
        keyboard=keyboard,
        state=state,
        message=message
    )
