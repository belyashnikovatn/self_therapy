#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable

from telebot import TeleBot, types, util
from selfcare.models import Person, PersonsHelpTip, PresetHelpTip, Emotion


class TelegramBot:
    """
    Bot can create an user, and after that using commands user can get emotion, get support or load preset.
    """
    def __init__(self, token):
        self._bot = TeleBot(token=token)
        self.start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.register_buttons(self.start_keyboard, [
            ('createuser', self.create_user),
            ('loadpreset', self.load_preset),
            ('getemotion', self.get_emotion),
            ('getsupport', self.get_support),
        ])
        self.register_command_handler(["start", "hi"], self.start_up)
        self._bot.callback_query_handler(func=lambda call: True)(self.add_support)

    def register_buttons(
        self,
        kbd: types.ReplyKeyboardMarkup,
        buttons: list[tuple[str, Callable[[types.Message], None]]]
    ):
        for btn in buttons:
            self.register_command_handler([btn[0]], btn[1])
        kbd.add(*[types.KeyboardButton('/'+btn[0]) for btn in buttons])

    def register_command_handler(
           self,
           commands: list[str],
           handler: Callable[[types.Message], None]
    ):
        self._bot.message_handler(commands=commands)(handler)

    def add_support(self, call):
        if call.data == 'addsupport':
            self._bot.send_message(call.from_user.id, text='Works')
        else:
            self._bot.send_message(call.from_user.id, text='Test not add supp')

    def create_user(self, message: types.Message):
        chat_id = message.chat.id
        name = message.chat.first_name
        Person.objects.get_or_create(
            tlg_id=chat_id,
            defaults={
                'name': name,
            }
        )
        self._bot.send_message(chat_id, text=f'User {name} created!')

    def load_preset(self, message: types.Message):
        chat_id = message.chat.id
        name = message.chat.first_name

        person, _ = Person.objects.get_or_create(
            tlg_id=chat_id,
            defaults={
                'name': name,
            }
        )
        helptips = PresetHelpTip.objects.all()
        bulk_list = []
        for tip in helptips:
            bulk_list.append(
                PersonsHelpTip(
                    text=tip.text,
                    person=person,
                    preset_tip=tip
                )
            )
        PersonsHelpTip.objects.bulk_create(bulk_list)
        self._bot.send_message(chat_id, text='Presets loaded!')

    def get_emotion(self, message: types.Message):
        emotion = Emotion.objects.order_by('?').first()
        text = emotion.name + '\n' + emotion.descriprion
        self._bot.send_message(message.chat.id, text=text)

    def get_support(self, message: types.Message):
        chat_id = message.chat.id
        name = message.chat.first_name
        # пока сделала так, чтобы рандомно, но нужно переделать
        person, _ = Person.objects.get_or_create(
            tlg_id=chat_id,
            defaults={
                'name': name,
            }
        )
        tip = person.personstips.order_by('?').first()
        text = tip.text
        self._bot.send_message(chat_id, text=text)

    def start_up(self, message: types.Message):
        chat = message.chat

        self._bot.send_message(
            chat_id=chat.id,
            text='Это режим разработки, поэтому все кнопки пока общим списком',
            reply_markup=self.start_keyboard
        )

    def infinity_polling(self):
        return self._bot.infinity_polling()
