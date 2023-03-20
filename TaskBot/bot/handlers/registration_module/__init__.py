from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd

from bot.filters import NotRegistered
from bot.handlers.registration_module import user_registration
from bot.states.Registration import UserRegistration


def setup(dp: Dispatcher):
    dp.register_message_handler(
        user_registration.start_registration,
        filters.CommandStart(),
        NotRegistered(),
        state="*",
    )
    dp.register_callback_query_handler(
        user_registration.get_main_registration_menu,
        filters.Text(cd.START_REG),
        state="*",
    )
    dp.register_callback_query_handler(
        user_registration.press_user_fio_or_phone,
        cd.reg.filter(),
        state=UserRegistration.MENU,
    )
    dp.register_message_handler(
        user_registration.get_user_fio, state=UserRegistration.FIO
    )
    dp.register_message_handler(
        user_registration.get_user_phone,
        state=UserRegistration.PHONE_NUMBER,
        content_types=types.ContentTypes.CONTACT
    )
    dp.register_callback_query_handler(
        user_registration.confirm_data,
        filters.Text(cd.DONE_REGISTRATION),
        state=UserRegistration.MENU,
    )
