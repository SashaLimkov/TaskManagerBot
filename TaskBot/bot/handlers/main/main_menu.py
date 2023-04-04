from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.handlers.main.faq import get_faq
from bot.handlers.main.granted_tasks import show_profile
from bot.handlers.main.tasks_menu import get_task_menu


async def main_menu_segregation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data["action"] == "1":
        await get_task_menu(call=call, state=state, callback_data=callback_data)
    elif callback_data["action"] == "2":
        await get_faq(call=call, state=state)
    else:
        await show_profile(message=call.message, state=state)
