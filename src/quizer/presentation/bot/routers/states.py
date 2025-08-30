from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    main = State()
    profile = State()
    my_surveys = State()


class CreateSurvey(StatesGroup):
    name = State()
    success = State()
