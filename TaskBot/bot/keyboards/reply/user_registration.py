from bot.utils.base_keyboard_utils import get_base_keyboard, get_keyboard_button

__all__ = [
    "get_phone_number",
]


async def get_phone_number():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
            "resize_keyboard": True
        },
        is_inline=False
    )
    keyboard.add(
        await get_keyboard_button(
            button={
                "text": "Отправить свой номер",
                "request_contact": True},
            is_inline=False
        )
    )
    return keyboard
