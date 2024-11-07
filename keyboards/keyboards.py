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
            KeyboardButton(text='💌 Похвалить себя')],
        [KeyboardButton(text='⚙ Кнопка настроек')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Выберите пункт меню 👇'
    )


def stop_fsm():
    kb_list = [
        [KeyboardButton(text='Галя, у нас отмена')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
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
        one_time_keyboard=False,
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
        one_time_keyboard=False,
        input_field_placeholder='Выберите пункт меню 👇'
    )


def selfesteem():
    kb_list = [
        [KeyboardButton(text='💌 Написать ещё')],
        [KeyboardButton(text='🗒 Дневник самооценки')],
        [KeyboardButton(text='🏠 Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Выберите пункт меню 👇'
    )
