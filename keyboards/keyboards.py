from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)


def main_kb():
    kb_list = [
        [KeyboardButton(text='❤‍🩹 Нужна помощь')],
        [
            KeyboardButton(text='👤 Что я чувствую'),
            KeyboardButton(text='🎉 Похвалить себя')],
        [
            KeyboardButton(text='⚙ Настройки'),
            KeyboardButton(text='📊 Статистика')
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню 👇'
    )


def stop_fsm():
    kb_list = [
        [KeyboardButton(text='❌ Отменить действие')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Можно отменить и вернуться в меню'
    )


def more_help():
    kb_list = [
        [KeyboardButton(text='❤‍🩹 Ещё совет')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню 👇'
    )


def mood():
    kb_list = [
        [KeyboardButton(text='🗒 Дневник эмоций')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню 👇'
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
        input_field_placeholder='Выберите пункт меню 👇'
    )


def short_texts_notes(notes):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for note in notes:
        button = InlineKeyboardButton(
            text=f'{note["date_created"]}: {note["text"][:15]}...',
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


def get_sets():
    kb_list = [
        [KeyboardButton(text='⭐ Как это работает')],
        [
            KeyboardButton(text='🗒 Дневник эмоций'),
            KeyboardButton(text='🗒 Дневник самооценки')],
        [
            KeyboardButton(text='❤ Список советов самопомощи'),
            KeyboardButton(text='🏠 Главное меню')
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню 👇'
    )
