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
    return builder.adjust(1).as_markup()
