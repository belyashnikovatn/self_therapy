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
        text='Поделиться настроением',
        callback_data='mood'
    ),
    builder.button(
        text='Похвалить себя',
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
        text='🏠 Главное меню',
        callback_data='start'
    )
    return builder.adjust(1).as_markup()


def after_mood() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Открыть дневник настроений',
        callback_data='mood_diary'
    ),
    builder.button(
        text='🏠 Главное меню',
        callback_data='start'
    )
    return builder.adjust(1).as_markup()


def after_selfesteem() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Похвалить себя ещё',
        callback_data='selfesteem'
    )
    builder.button(
        text='Открыть дневник похвалы',
        callback_data='selfesteem_diary'
    ),
    builder.button(
        text='🏠 Главное меню',
        callback_data='start'
    )
    return builder.adjust(1).as_markup()
