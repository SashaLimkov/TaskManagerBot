from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd
from . import main_menu, faq


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_menu.main_menu_segregation,
        cd.main_menu.filter(),
        state="*"
    )
