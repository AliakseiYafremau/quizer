from typing import Any
from uuid import UUID

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from quizer.application.dto.question import CreateQuestionDTO

from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import ManageSurvey, Menu
from quizer.logger import get_logger

logger = get_logger(__name__)


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


async def on_survey_error(
    message: Message, dialog_: Any, manager: DialogManager, error_: ValueError
):
    await message.answer("Название должно быть строкой!")


async def create_survey(
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
    await dialog_manager.switch_to(ManageSurvey.surveys_created)


async def pre_add_question(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    dialog_manager.dialog_data["question_name"] = data
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

    with ioc.add_question(id_provider) as interactor:
        await interactor(dto)
    await dialog_manager.switch_to(ManageSurvey.survey_menu)


async def get_survey_questions(dialog_manager: DialogManager, ioc: IoC, **kwargss):
    survey_id = dialog_manager.dialog_data["survey_id"]
    with ioc.get_surveys_questions() as interactor:
        questions = await interactor(survey_id)
    return {
        "questions": questions,
    }


async def get_user_surveys(ioc: IoC, id_provider: IdProvider, **kwargs):
    with ioc.get_user_surveys(id_provider) as interactor:
        surveys_data = await interactor()
    return {
        "surveys": surveys_data,
        "has_surveys": bool(surveys_data),
    }


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


manager_survey = Dialog(
    Window(
        Case(
            {
                True: Multi(
                    Const("Мои опросы:"),
                    List(Format("- {item.name}"), items="surveys"),
                ),
                False: Const("У вас нет опросов"),
            },
            selector="has_surveys",
        ),
        Start(
            Const("Создать новый опрос"),
            id="create_survey",
            state=ManageSurvey.create,
        ),
        Start(Const("Меню"), id="profile", state=Menu.main),
        getter=get_user_surveys,
        state=ManageSurvey.user_surveys,
    ),
    Window(
        Const("<b>Создание опроса</b>\n"),
        Const("Введите название нового <b>опроса</b>"),
        TextInput(
            id="survey_name",
            on_error=on_survey_error,
            on_success=create_survey,
            type_factory=str,
        ),
        state=ManageSurvey.create,
    ),
    Window(
        Const("<b>Новый опрос создан</b>\n"),
        Format("Название: <b>{dialog_data[survey_name]}</b>"),
        Const("Теперь вы можете добавить вопросы к вашему <b>опросу</b>"),
        ADD_QUESTION,
        MENU_BUTTON,
        state=ManageSurvey.surveys_created,
    ),
    Window(
        Const("<b>Добавление нового вопроса</b>\n"),
        Const("Введите вопрос"),
        TextInput(
            id="question_name",
            on_error=on_survey_error,
            on_success=pre_add_question,
            type_factory=str,
        ),
        state=ManageSurvey.add_question,
    ),
    Window(
        Format("<b>{dialog_data[survey_name]}</b>\n"),
        Const("Вопросы"),
        Format(" - {question_name} (не сохранен)"),
        List(Format("  - {item}"), items="options"),
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
    ),
    Window(
        Const("Введите опцию вопроса"),
        TextInput(
            id="option",
            on_error=on_survey_error,
            on_success=add_option,
            type_factory=str,
        ),
        state=ManageSurvey.option,
    ),
    Window(
        Const("Вопрос успешно создан, можете вернуться в меню или создать еще."),
        LOOK_SURVEY,
        ADD_QUESTION,
        MENU_BUTTON,
        state=ManageSurvey.create_question,
    ),
    Window(
        Const("Опрос успешно создан."),
        getter=get_survey_questions,
        state=ManageSurvey.survey_saved,
    )
)
