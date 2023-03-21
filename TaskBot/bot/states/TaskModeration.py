from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskModeration(StatesGroup):
    EX_USERNAME = State()
    OBS_USERNAME = State()
