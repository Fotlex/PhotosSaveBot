from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    default_state = State()
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_rename = State()
