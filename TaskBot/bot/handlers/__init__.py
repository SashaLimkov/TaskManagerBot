from aiogram import Dispatcher
from aiogram.dispatcher import filters
from bot.data import callback_data as cd
from . import registration_module, main, commands


def setup(dp: Dispatcher):
    registration_module.setup(dp)
    dp.register_message_handler(commands.start_command, filters.CommandStart(), state="*")
    main.setup(dp)
    dp.register_callback_query_handler(commands.main_menu, filters.Text(cd.MAIN_MENU), state="*")
    # main_module.setup(dp)
    # dp.register_message_handler(commands.start_command, filters.CommandStart(), state="*")
    # dp.register_callback_query_handler(commands.main_menu, filters.Text("mm"), state="*")
