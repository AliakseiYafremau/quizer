from typing import Any

from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start, SwitchTo


from quizer.presentation.bot.routers.states import ManageSurvey, Menu


async def on_survey_error(
    message: Message, dialog_: Any, manager: DialogManager, error_: ValueError
):
    await message.answer("Название должно быть строкой!")


MENU_BUTTON = Start(Const("Меню"), id="menu", state=Menu.main)
LOOK_SURVEY = SwitchTo(
    Const("Просмотреть опрос"),
    id="get_survey",
    state=ManageSurvey.surveys_created,
)
ADD_QUESTION = SwitchTo(
    Const("Добавить вопрос"), id="add_question", state=ManageSurvey.add_question
)
SAVE_SURVEY = SwitchTo(
    Const("Сохранить опрос"), id="save_survey", state=ManageSurvey.survey_menu
)
