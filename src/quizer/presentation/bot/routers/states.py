from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    main = State()
    profile = State()
    my_surveys = State()


class ManageSurvey(StatesGroup):
    user_surveys = State()
    create = State()
    surveys_created = State()
    add_question = State()
    question_name = State()
    option = State()
    create_question = State()