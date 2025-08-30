from typing import Any

from aiogram.types import Message

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import CreateSurvey, Menu
from quizer.logger import get_logger

logger = get_logger(__name__)


async def error(
    message: Message, dialog_: Any, manager: DialogManager, error_: ValueError
):
    await message.answer("Название должно быть строкой!")


async def on_survey_enter(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    ioc: IoC = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]
    with ioc.create_survey(id_provider) as interactor:
        survey_id = await interactor(data)
    dialog_manager.dialog_data["survey_id"] = survey_id
    dialog_manager.dialog_data["survey_name"] = data
    await dialog_manager.switch_to(CreateSurvey.success)


async def get_survey_questions(dialog_manager: DialogManager, ioc: IoC, **kwargss):
    survey_id = dialog_manager.dialog_data["survey_id"]
    with ioc.get_surveys_questions() as interactor:
        questions = await interactor(survey_id)
    return {
        "questions": questions,
    }


create_survey = Dialog(
    Window(
        Const("Введите название опроса"),
        TextInput(
            id="name",
            on_error=error,
            on_success=on_survey_enter,
            type_factory=str,
        ),
        state=CreateSurvey.name,
    ),
    Window(
        Format('Опрос создан "{dialog_data[survey_name]}".'),
        Start(Const("Меню"), id="menu", state=Menu.main),
        getter=get_survey_questions,
        state=CreateSurvey.success,
    ),
)
