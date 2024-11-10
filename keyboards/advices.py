from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from constants import ADVICE_LENGTH



def advice():
    kb_list = [
        [KeyboardButton(text='💔 Ещё совет')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню'
    )


def advices_list(advices):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for advice in advices:
        button = InlineKeyboardButton(
            text=f'{advice["date_created"]}: {advice["text"][:ADVICE_LENGTH]}...',
            callback_data=f'manage_note_{advice["id"]}'
        )
        keyboard.inline_keyboard.append([button])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu')
        ])
    return keyboard


def manage_advice(advice_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Изменить текст',
                callback_data=f'edit_advice_{advice_id}')],
            [InlineKeyboardButton(
                text='Удалить',
                callback_data=f'delete_advice_{advice_id}')]
        ]
    )
