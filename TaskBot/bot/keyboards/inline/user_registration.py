from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_start_registration_keyboard",
    "get_user_registration_menu",
]


async def get_start_registration_keyboard():
    return await get_base_keyboard(
        buttons=[
            {"text": "Начать регистрацию", "callback_data": cd.START_REG},
        ]
    )


async def get_user_registration_menu(done: bool = False):
    buttons = [
        {"text": "ФИО", "callback_data": cd.reg.new(action=1)},
        {"text": "Номер телефона", "callback_data": cd.reg.new(action=2)},
    ]
    if done:
        buttons.append({"text": "Продолжить", "callback_data": cd.DONE_REGISTRATION})
    return await get_base_keyboard(
        buttons=buttons,
        keyboard_options={
            "row_width": 1,
        },
    )

