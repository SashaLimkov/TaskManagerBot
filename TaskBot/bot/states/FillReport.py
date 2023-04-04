from aiogram.dispatcher.filters.state import StatesGroup, State


class FillReportState(StatesGroup):
    FIlE = State()
    TEXT = State()
    MENU = State()
