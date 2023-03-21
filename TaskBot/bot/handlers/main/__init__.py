from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd
from . import main_menu, faq, tasks_menu, task_creation, task_moderation
from ...states.TaskCreation import TaskCreation
from ...states.TaskModeration import TaskModeration


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        main_menu.main_menu_segregation,
        cd.main_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        tasks_menu.tasks_menu_segregation,
        cd.task_menu_actions.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        task_creation.task_create_segregation,
        cd.task_creation_menu.filter(),
        state="*"
    )
    dp.register_message_handler(
        task_creation.get_task_description,
        state=TaskCreation.DESCRIPTION
    )
    dp.register_message_handler(
        task_creation.get_task_date_time,
        state=TaskCreation.DATE_TIME
    )
    dp.register_message_handler(
        task_creation.get_task_file,
        state=TaskCreation.FILE,
        content_types=types.ContentTypes.DOCUMENT,
    )
    dp.register_message_handler(
        task_creation.get_task_file,
        state=TaskCreation.FILE,
    )
    dp.register_callback_query_handler(
        task_moderation.moderate_task_menu_call,
        cd.task_moderation_list.filter(),
        state="*",
    )
    dp.register_callback_query_handler(
        task_moderation.segregate_task_moderation_menu,
        cd.task_moderation_menu.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        task_moderation.close_task,
        filters.Text(startswith="clt_"),
        state="*"
    )
    dp.register_callback_query_handler(
        task_moderation.task_moderation_change_task_segregator_call,
        cd.task_moderation_change_menu.filter(),
        state="*"
    )
    dp.register_message_handler(
        task_moderation.update_task_description,
        state=TaskCreation.UPDATE_DESCRIPTION
    )
    dp.register_message_handler(
        task_moderation.update_task_date_time,
        state=TaskCreation.UPDATE_DATE_TIME
    )
    dp.register_message_handler(
        task_moderation.update_task_file,
        state=TaskCreation.UPDATE_FILE,
        content_types=types.ContentTypes.DOCUMENT,
    )
    dp.register_message_handler(
        task_moderation.update_task_file,
        state=TaskCreation.UPDATE_FILE,
    )
    dp.register_message_handler(
        task_moderation.get_ex_username,
        state=TaskModeration.EX_USERNAME
    )
    dp.register_message_handler(
        task_moderation.get_obs_username,
        state=TaskModeration.OBS_USERNAME
    )
