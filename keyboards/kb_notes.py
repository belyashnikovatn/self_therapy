from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from constants import NOTE_LENGTH


def mood():
    kb_list = [
        [KeyboardButton(text='👤 Написать ещё')],
        [KeyboardButton(text='🗒 Дневник эмоций')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню'
    )


def selfesteem():
    kb_list = [
        [KeyboardButton(text='🎉 Написать ещё')],
        [KeyboardButton(text='🗒 Дневник самооценки')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню'
    )


def notes_list(notes):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for note in notes:
        button = InlineKeyboardButton(
            text=f'{note["date_created"]}: {note["text"][:NOTE_LENGTH]}...',
            callback_data=f'manage_note_{note["id"]}'
        )
        keyboard.inline_keyboard.append([button])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='main_menu')
        ])
    return keyboard


def manage_note(note_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Изменить текст',
                callback_data=f'edit_note_{note_id}')],
            [InlineKeyboardButton(
                text='Удалить',
                callback_data=f'delete_note_{note_id}')]
        ]
    )
