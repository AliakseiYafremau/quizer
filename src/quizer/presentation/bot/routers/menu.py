from aiogram.fsm.state import StatesGroup, State

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.presentation.ioc import IoC


class Menu(StatesGroup):
    main = State()
    profile = State()
    my_surveys = State()


async def get_user_data(ioc: IoC, id_provider: IdProvider):
    with ioc.get_user(id_provider) as interactor:
        user_data = await interactor()
    return {
        "user_id": user_data.id,
        "username": user_data.name,
    }


async def get_user_surveys(ioc: IoC):
    pass


menu_dialog = Dialog(
    Window(
        Const("Привет. С помощью этого бота ты можешь создавать или проходить опросы!"),
        SwitchTo(Const("Профиль"), id="profile", state=Menu.profile),
        SwitchTo(Const("Мои опросы"), id="surveys", state=Menu.my_surveys),
        state=Menu.main,
    ),
    Window(
        Const("Информация о пользователе:"),
        Format("ID пользователя: {user_id}"),
        Format("Имя пользователя: {username}"),
        getter=get_user_data,
        state=Menu.profile,
    ),
)
