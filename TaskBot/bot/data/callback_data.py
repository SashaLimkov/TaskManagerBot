from aiogram.utils.callback_data import CallbackData

START_REG = "start_reg"
DONE_REGISTRATION = "done_reg"
TASKS_MENU = "tasks_menu"
TASK = "task_pk"
MY_TASKS = "my_tasks"
FAQ = "faq"
MAIN_MENU = "mm"
ACTION = "action"

reg = CallbackData("reg", ACTION)
main_menu = CallbackData(MAIN_MENU, ACTION)
task_menu_actions = CallbackData(TASKS_MENU, ACTION, f"{ACTION}_2")
task_creation_menu = CallbackData(TASKS_MENU, ACTION, f"{ACTION}_2", f"{ACTION}_3")
task_moderation_list = CallbackData(TASKS_MENU + "m", ACTION, f"{ACTION}_2", TASK)
task_moderation_menu = CallbackData(TASKS_MENU, ACTION, f"{ACTION}_2", TASK, f"{ACTION}_3")
task_moderation_change_menu = CallbackData(TASKS_MENU + "c", ACTION, f"{ACTION}_2", TASK, f"{ACTION}_3")
