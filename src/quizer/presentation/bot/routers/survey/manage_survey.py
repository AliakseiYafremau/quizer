
from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button


from quizer.presentation.bot.routers.survey.survey_creation import (
    survey_creation,
    survey_created,
)
from quizer.presentation.bot.routers.survey.question_creation import (
    question_creation,
    current_question,
    option_creation,
    finish_question,
)
from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import ManageSurvey

from quizer.presentation.bot.routers.survey.survey_list import survey_list


async def save_survey(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    ioc: IoC = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]

    survey_id = dialog_manager.dialog_data["survey_id"]

    async with ioc.save_survey(id_provider=id_provider) as interactor:
        await interactor(survey_id)

    await dialog_manager.switch_to(ManageSurvey.user_surveys)


async def get_survey_questions(dialog_manager: DialogManager, ioc: IoC, **kwargss):
    survey_id = dialog_manager.dialog_data["survey_id"]
    async with ioc.get_surveys_questions() as interactor:
        questions = await interactor(survey_id)
    return {
        "questions": questions,
    }




manager_survey = Dialog(
    survey_list,
    survey_creation,
    survey_created,
    question_creation,
    current_question,
    option_creation,
    finish_question,
    Window(
        Const("Опрос успешно создан."),
        getter=get_survey_questions,
        state=ManageSurvey.survey_saved,
    ),
)
