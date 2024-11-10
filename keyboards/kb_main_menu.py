from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


def main_kb():
    kb_list = [
        [KeyboardButton(text='💔 Нужна помощь')],
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
        input_field_placeholder='Выберите пункт меню'
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
        input_field_placeholder='Выберите пункт меню'
    )

