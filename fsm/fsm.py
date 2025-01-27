from aiogram.fsm.state import State, StatesGroup


class FSMStyleGen(StatesGroup):
    first_photo = State()
    second_photo = State()
