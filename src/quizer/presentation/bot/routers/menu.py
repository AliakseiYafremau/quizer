from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Start

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.presentation.ioc import IoC
from quizer.presentation.bot.routers.states import Menu, ManageSurvey


async def get_user_data(ioc: IoC, id_provider: IdProvider, **kwargs):
    with ioc.get_user(id_provider) as interactor:
        user_data = await interactor()
    return {
        "user_id": user_data.id,
        "username": user_data.name,
    }


menu_dialog = Dialog(
    Window(
        Const("Привет. С помощью этого бота ты можешь создавать или проходить опросы!"),
        SwitchTo(Const("Профиль"), id="profile", state=Menu.profile),
        Start(Const("Мои опросы"), id="surveys", state=ManageSurvey.user_surveys),
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
)
