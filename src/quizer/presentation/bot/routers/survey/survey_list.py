from aiogram_dialog import Window

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from aiogram_dialog.widgets.kbd import Start

from quizer.presentation.bot.routers.states import ManageSurvey, Menu

from quizer.presentation.ioc import IoC
from quizer.presentation.bot.id_provider import IdProvider


async def get_user_surveys(ioc: IoC, id_provider: IdProvider, **kwargs):
    async with ioc.get_user_surveys(id_provider) as interactor:
        surveys_data = await interactor()
    return {
        "surveys": surveys_data,
        "has_surveys": bool(surveys_data),
    }


survey_list = Window(
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
)
