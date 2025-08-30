from typing import Any

from aiogram.types import Message

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from aiogram_dialog.widgets.kbd import Start, Next, SwitchTo, Back
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider
from quizer.presentation.bot.routers.states import ManageSurvey, Menu
from quizer.logger import get_logger

logger = get_logger(__name__)


async def on_survey_error(
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
    await dialog_manager.switch_to(ManageSurvey.surveys_created)


async def on_option_enter(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    current_options = dialog_manager.dialog_data.get("options", [])
    current_options.append(dialog_manager.find("option").get_value())
    dialog_manager.dialog_data["options"] = current_options
    await dialog_manager.switch_to(ManageSurvey.question_name)


async def on_question_enter(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
):
    ioc: IoC = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]
    with ioc.add_question(id_provider) as interactor:
        await interactor()


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


async def get_question_name(
    dialog_manager: DialogManager, ioc: IoC, **kwargs,
):
    options = dialog_manager.dialog_data.get("options", [])
    return {
        "question_name": dialog_manager.find("question_name").get_value(),
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
            Const("Создать новый опрос"), id="create_survey", state=ManageSurvey.create,
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
            on_success=on_survey_enter,
            type_factory=str,
        ),
        parse_mode="html",
        state=ManageSurvey.create,
    ),
    Window(
        Const("<b>Создание опроса</b>\n"),
        Format("Название: <b>{dialog_data[survey_name]}</b>"),
        SwitchTo(Const("Добавить вопрос"), id="add_question", state=ManageSurvey.add_question),
        Start(Const("Меню"), id="menu", state=Menu.main),
        parse_mode="html",
        getter=get_survey_questions,
        state=ManageSurvey.surveys_created,
    ),
    Window(
        Const("Введите вопрос"),
        TextInput(
            id="question_name",
            on_error=on_survey_error,
            on_success=Next(),
            type_factory=str,
        ),
        state=ManageSurvey.add_question,
    ),
    Window(
        Const("<b>Создание опроса</b>\n"),
        Format("Название: <b>{dialog_data[survey_name]}</b>\n"),
        Const("Вопросы"),
        Format(" - {question_name} (не сохранен)"),
        List(Format("  - {item}"), items="options"),
        SwitchTo(Const("Просмотреть опрос"), id="get_survey", state=ManageSurvey.surveys_created),
        SwitchTo(Const("Добавить опцию"), id="add_question", state=ManageSurvey.option),
        SwitchTo(Const("Сохранить вопрос"), id="save_question", state=ManageSurvey.create_question),
        Start(Const("Меню"), id="menu", state=Menu.main),
        parse_mode="html",
        getter=get_question_name, # После возвращать все вопросы + question_name не сохраненный
        state=ManageSurvey.question_name,
    ),
    Window(
        Const("Введите опцию вопроса"),
        TextInput(
            id="option",
            on_error=on_survey_error,
            on_success=on_option_enter,
            type_factory=str,
        ),
        parse_mode="html",
        state=ManageSurvey.option,
    ),
    Window(
        Const("Вопрос успешно создан, можете вернуться в меню или создать еще."),
        SwitchTo(Const("Просмотреть опрос"), id="get_survey", state=ManageSurvey.surveys_created),
        SwitchTo(Const("Добавить вопрос"), id="add_question", state=ManageSurvey.add_question),
        Start(Const("Меню"), id="menu", state=Menu.main),
        parse_mode="html",
        state=ManageSurvey.create_question,
    )
)
