from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_main_menu",
    "get_faq",
    "get_main_tasks_menu"
]


async def get_main_menu():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Задачи", cd=cd.main_menu.new(
                action=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Справочник", cd=cd.main_menu.new(
                action=2
            )
        )
    )
    return keyboard


async def get_main_tasks_menu(callback_data):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Создать задачу", cd=cd.task_menu_actions.new(
                action=callback_data["action"],
                action_2=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Созданные задачи", cd=cd.task_menu_actions.new(
                action=callback_data["action"],
                action_2=2

            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Назначенные задачи", cd=cd.task_menu_actions.new(
                action=callback_data["action"],
                action_2=3
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.MAIN_MENU
        )
    )
    return keyboard


async def get_faq():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.MAIN_MENU
        )
    )
    return keyboard
