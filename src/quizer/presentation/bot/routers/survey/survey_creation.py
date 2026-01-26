from aiogram.types import Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput


from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import ManageSurvey

from quizer.presentation.bot.routers.survey.common import (
    on_survey_error,
    ADD_QUESTION,
    MENU_BUTTON,
)


async def create_survey(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    ioc: IoC = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]

    async with ioc.create_survey(id_provider) as interactor:
        survey_id = await interactor(data)
    dialog_manager.dialog_data["survey_id"] = survey_id
    dialog_manager.dialog_data["survey_name"] = data
    await dialog_manager.switch_to(ManageSurvey.surveys_created)


survey_creation = Window(
    Const("<b>Создание опроса</b>\n"),
    Const("Введите название нового <b>опроса</b>"),
    TextInput(
        id="survey_name",
        on_error=on_survey_error,
        on_success=create_survey,
        type_factory=str,
    ),
    state=ManageSurvey.create,
)

survey_created = Window(
    Const("<b>Новый опрос создан</b>\n"),
    Format("Название: <b>{dialog_data[survey_name]}</b>"),
    Const("Теперь вы можете добавить вопросы к вашему <b>опросу</b>"),
    ADD_QUESTION,
    MENU_BUTTON,
    state=ManageSurvey.surveys_created,
)
