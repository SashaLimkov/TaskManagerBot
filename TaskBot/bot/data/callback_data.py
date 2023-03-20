from aiogram.utils.callback_data import CallbackData

START_REG = "start_reg"
DONE_REGISTRATION = "done_reg"
TASKS_MENU = "tasks_menu"
MY_TASKS = "my_tasks"
FAQ = "faq"
MAIN_MENU = "mm"
ACTION = "action"

reg = CallbackData("reg", ACTION)
main_menu = CallbackData(MAIN_MENU, ACTION)
task_menu_actions = CallbackData(TASKS_MENU, ACTION, f"{ACTION}_2")

