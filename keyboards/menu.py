from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    """Generate main menu"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Мне нужна помощь',
        callback_data='support'
    ),
    builder.button(
        text='Дневник настроения',
        callback_data='mood'
    ),
    builder.button(
        text='Дневник самооценки',
        callback_data='selfesteem'
    ),
    builder.button(
        text='Узнать данные',
        callback_data='get_data'
    ),
    return builder.adjust(1).as_markup()


def get_more_help() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Ещё',
        callback_data='support'
    ),
    builder.button(
        text='Главное меню',
        callback_data='start'
    )
    return builder.adjust(1).as_markup()
