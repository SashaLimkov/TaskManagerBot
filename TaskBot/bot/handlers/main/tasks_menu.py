from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.data import text_data as td
from bot.handlers.main.task_creation import create_task_menu
from bot.handlers.main.task_moderation import created_tasks_list_menu
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
    else:
        pass
