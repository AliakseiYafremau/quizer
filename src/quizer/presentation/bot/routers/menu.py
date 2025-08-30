from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Multi, List, Case
from aiogram_dialog.widgets.kbd import SwitchTo, Start

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.presentation.ioc import IoC
from quizer.presentation.bot.routers.create_survey import CreateSurvey
from quizer.presentation.bot.routers.states import Menu, CreateSurvey


async def get_user_data(ioc: IoC, id_provider: IdProvider, **kwargs):
    with ioc.get_user(id_provider) as interactor:
        user_data = await interactor()
    return {
        "user_id": user_data.id,
        "username": user_data.name,
    }


async def get_user_surveys(ioc: IoC, id_provider: IdProvider, **kwargs):
    with ioc.get_user_surveys(id_provider) as interactor:
        surveys_data = await interactor()
    return {
        "surveys": surveys_data,
        "has_surveys": bool(surveys_data),
    }


menu_dialog = Dialog(
    Window(
        Const("Привет. С помощью этого бота ты можешь создавать или проходить опросы!"),
        SwitchTo(Const("Профиль"), id="profile", state=Menu.profile),
        SwitchTo(Const("Мои опросы"), id="surveys", state=Menu.my_surveys),
        state=Menu.main,
    ),
    Window(
        Const("Информация о пользователе:"),
        Format("  - ID пользователя: {user_id}"),
        Format("  - Имя пользователя: {username}"),
        SwitchTo(Const("Меню"), id="profile", state=Menu.main),
        getter=get_user_data,
        state=Menu.profile,
    ),
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
            Const("Создать новый опрос"), id="create_survey", state=CreateSurvey.name
        ),
        SwitchTo(Const("Меню"), id="profile", state=Menu.main),
        getter=get_user_surveys,
        state=Menu.my_surveys,
    ),
)
