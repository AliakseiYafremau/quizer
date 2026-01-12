from uuid import UUID

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from quizer.application.dto.question import CreateQuestionDTO

from quizer.presentation.bot.routers.survey.common import (
    on_survey_error,
    ADD_QUESTION,
    MENU_BUTTON,
    LOOK_SURVEY,
)
from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import ManageSurvey



async def pre_add_question(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    dialog_manager.dialog_data["question_name"] = data
    dialog_manager.dialog_data["options"] = []
    await dialog_manager.switch_to(ManageSurvey.survey_menu)


async def add_option(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    current_options = dialog_manager.dialog_data.get("options", [])
    current_options.append(data)
    dialog_manager.dialog_data["options"] = current_options
    await dialog_manager.switch_to(ManageSurvey.survey_menu)


async def add_question(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    ioc: IoC = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]

    survey_id: UUID = dialog_manager.dialog_data["survey_id"]
    question_name: str = dialog_manager.dialog_data["question_name"]
    options: list[str] = dialog_manager.dialog_data["options"]

    dto = CreateQuestionDTO(survey_id=survey_id, name=question_name, options=options)

    async with ioc.add_question(id_provider) as interactor:
        await interactor(dto)

    del dialog_manager.dialog_data["question_name"]
    del dialog_manager.dialog_data["options"]

    await dialog_manager.switch_to(ManageSurvey.survey_menu)


async def get_question(
    dialog_manager: DialogManager,
    ioc: IoC,
    **kwargs,
):
    question_name = dialog_manager.dialog_data["question_name"]
    options = dialog_manager.dialog_data.get("options", [])
    return {
        "question_name": question_name,
        "options": options,
    }

question_creation =Window(
        Const("<b>Добавление нового вопроса</b>\n"),
        Const("Введите вопрос"),
        TextInput(
            id="question_name",
            on_error=on_survey_error,
            on_success=pre_add_question,
            type_factory=str,
        ),
        state=ManageSurvey.add_question,
    )

current_question = Window(
        Format("<b>{dialog_data[survey_name]}</b>\n"),
        Const("Вопросы"),
        Format(" - {question_name} (не сохранен)"),
        List(Format("    - {item}"), items="options"),
        SwitchTo(Const("Добавить опцию"), id="add_option", state=ManageSurvey.option),
        SwitchTo(
            Const("Сохранить вопрос"),
            id="save_question",
            on_click=add_question,
            state=ManageSurvey.create_question,
        ),
        MENU_BUTTON,
        getter=get_question,  # После возвращать все вопросы + question_name не сохраненный
        state=ManageSurvey.survey_menu,
    )
option_creation =Window(
        Const("Введите опцию вопроса"),
        TextInput(
            id="option",
            on_error=on_survey_error,
            on_success=add_option,
            type_factory=str,
        ),
        state=ManageSurvey.option,
    )


finish_question =Window(
        Const("Вопрос успешно создан, можете вернуться в меню или создать еще."),
        LOOK_SURVEY,
        ADD_QUESTION,
        MENU_BUTTON,
        state=ManageSurvey.create_question,
    )
