from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskCreation(StatesGroup):
    MENU = State()
    DESCRIPTION = State()
    DATE_TIME = State()
    FILE = State()
    UPDATE_DESCRIPTION = State()
    UPDATE_DATE_TIME = State()
    UPDATE_FILE = State()