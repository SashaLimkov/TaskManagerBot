from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.utils.message_worker import dry_message_editor


async def get_faq(call: types.CallbackQuery, state: FSMContext):
    await dry_message_editor(
        text=td.FAQ,
        keyboard=await ik.get_faq(),
        state=state,
        message=call.message
    )
