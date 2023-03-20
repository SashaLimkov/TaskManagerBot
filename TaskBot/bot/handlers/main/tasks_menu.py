from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.data import text_data as td
from bot.handlers.main.faq import get_faq
from bot.keyboards import inline as ik
from bot.utils.message_worker import dry_message_editor


async def get_task_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await dry_message_editor(
        text=td.TASKS_MENU,
        keyboard=await ik.get_main_tasks_menu(callback_data=callback_data),
        state=state,
        message=call.message
    )


async def tasks_menu_segregation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data["action_2"] == "1":
        pass
    elif callback_data["action_2"] == "2":
        pass
    else:
        pass


async def create_task_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    pass