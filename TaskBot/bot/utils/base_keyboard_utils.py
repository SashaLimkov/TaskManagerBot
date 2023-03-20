from aiogram import types

__all__ = ["get_base_keyboard", "get_inline_button"]


async def get_inline_button(text: str, cd: str = None, url: str = None):
    return (
        types.InlineKeyboardButton(text=text, url=url)
        if url
        else types.InlineKeyboardButton(
            text=text,
            callback_data=cd,
        )
    )


async def get_base_keyboard(
    buttons: list = [], keyboard_options: dict = {}, is_inline: bool = True
) -> types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup:
    """
    :param buttons: list of json for buttons with button_options
    :param keyboard_options: keyboard_options
    :param is_inline: bool argument for creating inline or reply keyboard markup
    :return: keyboard json obj
    """
    keyboard = await get_keyboard_markup(
        keyboard_options=keyboard_options, is_inline=is_inline
    )
    for button in buttons:
        keyboard.insert(await get_keyboard_button(button=button, is_inline=is_inline))
    return keyboard


async def get_keyboard_markup(
    keyboard_options: dict, is_inline: bool
) -> types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup:
    """
    :param keyboard_options: keyboard_options
    :param is_inline: bool argument for creating inline or reply keyboard markup
    :return: keyboard markup obj
    """
    return (
        types.InlineKeyboardMarkup(**keyboard_options)
        if is_inline
        else types.ReplyKeyboardMarkup(**keyboard_options)
    )


async def get_keyboard_button(
    button: dict, is_inline: bool
) -> types.InlineKeyboardButton | types.KeyboardButton:
    """
    :param button: button options
    :param is_inline: bool argument for creating inline or reply button
    :return: keyboard button obj
    """
    return (
        types.InlineKeyboardButton(**button)
        if is_inline
        else types.KeyboardButton(**button)
    )
