from backend.services.task import get_created_tasks
from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd
from bot.data.callback_data import ACTION

__all__ = [
    "get_main_menu",
    "get_faq",
    "get_main_tasks_menu",
    "get_create_task_menu",
    "get_created_tasks_list",
    "get_task_moderation_menu",
    "close_task_menu",
    "edit_task_menu"
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
                action=callback_data[ACTION],
                action_2=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Созданные задачи", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
                action_2=2

            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Назначенные задачи", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
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


async def get_create_task_menu(callback_data: dict, done: bool):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить описание", cd=cd.task_creation_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                action_3=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить файл", cd=cd.task_creation_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                action_3=2
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Дата и время", cd=cd.task_creation_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                action_3=3
            )
        )
    )
    if done:
        keyboard.add(
            await get_inline_button(
                text="Продолжить", cd=cd.task_creation_menu.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    action_3=4
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.main_menu.new(
                action=1
            )
        )
    )
    return keyboard


async def get_created_tasks_list(callback_data: dict, telegram_id):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    tasks = get_created_tasks(telegram_id=telegram_id)
    for task in tasks:
        keyboard.add(
            await get_inline_button(
                text=f"{task.pk}", cd=cd.task_moderation_list.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=task.pk,
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.main_menu.new(
                action=callback_data[ACTION],
            )
        )
    )
    return keyboard


async def get_task_moderation_menu(callback_data: dict, task: int = 0):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Список исполнителей", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task or callback_data[cd.TASK],
                action_3=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Список наблюдателей", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task or callback_data[cd.TASK],
                action_3=2
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Изменить задачу", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task or callback_data[cd.TASK],
                action_3=3
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Закрыть задачу", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task or callback_data[cd.TASK],
                action_3=4
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
                action_2=2
            )
        )
    )
    return keyboard


async def close_task_menu(callback_data):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Подтвердить закрытие задачи", cd=f"clt_{callback_data[cd.TASK]}"
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.task_moderation_list.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[cd.TASK],
            )
        )
    )
    return keyboard


async def edit_task_menu(callback_data):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Изменить описание", cd=cd.task_moderation_change_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=callback_data[cd.TASK],
                action_3=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Изменить дату и время", cd=cd.task_moderation_change_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=callback_data[cd.TASK],
                action_3=2
            ))
    )
    keyboard.add(
        await get_inline_button(
            text="Заменить файл", cd=cd.task_moderation_change_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=callback_data[cd.TASK],
                action_3=3
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.task_moderation_list.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[cd.TASK],
            )
        )
    )
    return keyboard
