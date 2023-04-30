from backend.services.task import get_created_tasks, get_granted_tasks
from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd
from bot.data.callback_data import ACTION, TASK

__all__ = [
    "get_main_menu",
    "get_faq",
    "get_main_tasks_menu",
    "get_create_task_menu",
    "get_created_tasks_list",
    "get_task_moderation_menu",
    "close_task_menu",
    "edit_task_menu",
    "back_to_mm",
    "get_granted_tasks_list",
    "granted_task_menu",
    "report_fill_menu",
    "back_to_granted_task_report_menu",
    "back_to_tasks_menu",
    "back_to_find_tasks_menu",
    "executors_list",
    "back_to_executors_list"
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
    keyboard.add(
        await get_inline_button(
            text="Профиль", cd=cd.main_menu.new(
                action=3
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
            text="Найти задачу по номеру", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
                action_2=4
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
                text=f"{task.pk} {task.task[:15]}...", cd=cd.task_moderation_list.new(
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
    task_pk = task or callback_data[cd.TASK]
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить/удалить исполнителей", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task_pk,
                action_3=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Список наблюдателей", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task_pk,
                action_3=2
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Просмотреть исполнителей", cd=cd.granted_obs_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=task_pk,
                action_3=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Изменить задачу", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task_pk,
                action_3=3
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Закрыть задачу", cd=cd.task_moderation_menu.new(
                action=callback_data[ACTION],
                action_2=2,
                task_pk=task_pk,
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


async def back_to_mm():
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


async def get_granted_tasks_list(callback_data: dict, telegram_id):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    tasks = get_granted_tasks(telegram_id=telegram_id)
    for task in tasks:
        keyboard.add(
            await get_inline_button(
                text=f"{task.task.pk} {task.task.task[:15]}... {'✅' if task.is_done else ''}", cd=cd.granted_task_list.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=task.task.pk,
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


async def granted_task_menu(callback_data: dict, executor: bool = True, done: bool = False):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    if executor and not done:
        keyboard.add(
            await get_inline_button(
                text="Заполнить отчет", cd=cd.granted_task_menu.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=callback_data[TASK],
                    action_3=1
                )
            )
        )
    else:
        keyboard.add(
            await get_inline_button(
                text="Просмотреть исполнителей", cd=cd.granted_obs_menu.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=callback_data[TASK],
                    action_3=1
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
                action_2=3
            )
        )
    )
    return keyboard


async def report_fill_menu(callback_data: dict, any_of_fields: bool):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить текст", cd=cd.granted_task_report_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[TASK],
                action_3=callback_data[f"{ACTION}_3"],
                action_4=1
            )
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Добавить файл", cd=cd.granted_task_report_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[TASK],
                action_3=callback_data[f"{ACTION}_3"],
                action_4=2
            )
        )
    )
    if any_of_fields:
        keyboard.add(
            await get_inline_button(
                text="Отправить отчет", cd=cd.granted_task_report_menu.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=callback_data[TASK],
                    action_3=callback_data[f"{ACTION}_3"],
                    action_4=3
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.granted_task_list.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[TASK]

            )
        )
    )
    return keyboard


async def back_to_granted_task_report_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.granted_task_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[TASK],
                action_3=callback_data[f"{ACTION}_3"]
            )
        )
    )
    return keyboard


async def back_to_tasks_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.main_menu.new(
                action=callback_data[ACTION],
            )
        )
    )
    return keyboard


async def back_to_find_tasks_menu(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.main_menu.new(
                action=callback_data[ACTION],
            )
        )
    )
    return keyboard


async def executors_list(task, callback_data):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    executors = task.executors.filter(role__name="Исполнитель").all()
    for executor in executors:
        keyboard.add(
            await get_inline_button(
                text=executor.user.fio,
                cd=cd.granted_obs_executors_menu.new(
                    action=callback_data[ACTION],
                    action_2=callback_data[f"{ACTION}_2"],
                    task_pk=callback_data[TASK],
                    action_3=callback_data[f"{ACTION}_3"],
                    user_pk=executor.user.pk
                )
            )
        )
    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.task_menu_actions.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
            )
        )
    )
    return keyboard


async def back_to_executors_list(callback_data: dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )

    keyboard.add(
        await get_inline_button(
            text="◀ Назад", cd=cd.granted_obs_menu.new(
                action=callback_data[ACTION],
                action_2=callback_data[f"{ACTION}_2"],
                task_pk=callback_data[TASK],
                action_3=callback_data[f"{ACTION}_3"]
            )
        )
    )
    return keyboard
