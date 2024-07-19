"""Main telegram-bot logic & funcs."""

import os
import requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from selfcare.models import Person, PersonsHelpTip, PresetHelpTip, Emotion

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


class Command(BaseCommand):
    """Create custom django-admin commands."""

    help = 'Telegram bot for selfcare'

    def handle(self, *args, **options):
        """Make a bot and start work."""
        bot = TeleBot(token=BOT_TOKEN)
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # start_keyboard = types.InlineKeyboardMarkup()
        btn_create_user = types.KeyboardButton('/createuser')
        btn_loadpreset = types.KeyboardButton('/loadpreset')
        btn_getemotion = types.KeyboardButton('/getemotion')
        btn_getsupport = types.KeyboardButton('/getsupport')
        # btn_addsupport = types.InlineKeyboardButton('Можно русским языком',
        #                                             callback_data='addsupport')
        # start_keyboard.add(btn_addsupport)
        start_keyboard.add(btn_create_user, btn_loadpreset,
                           btn_getemotion, btn_getsupport)

        @bot.callback_query_handler(func=lambda call: True)
        def add_support(call):
            if call.data == 'addsupport':
                bot.send_message(call.from_user.id, text='Works')
            else:
                bot.send_message(call.from_user.id, text='Test not add supp')

        @bot.message_handler(commands=['createuser'])
        def create_user(message):
            chat_id = message.chat.id
            name = message.chat.first_name
            Person.objects.get_or_create(
                tlg_id=chat_id,
                defaults={
                    'name': name,
                }
            )
            bot.send_message(chat_id, text=f'User {name} created!')

        @bot.message_handler(commands=['loadpreset'])
        def load_preset(message):
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
            bot.send_message(chat_id, text='Presets loaded!')

        @bot.message_handler(commands=['getemotion'])
        def get_emotion(message):
            emotion = Emotion.objects.order_by('?').first()
            text = emotion.name + '\n' + emotion.descriprion
            bot.send_message(message.chat.id, text=text)

        @bot.message_handler(commands=['getsupport'])
        def get_support(message):
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
            bot.send_message(chat_id, text=text)

        @bot.message_handler(commands=['start', 'hi'])
        def start_up(message):
            chat = message.chat

            bot.send_message(
                chat_id=chat.id,
                text='Это режим разработки, поэтому все кнопки пока общим списком',
                reply_markup=start_keyboard
            )

        bot.infinity_polling()
