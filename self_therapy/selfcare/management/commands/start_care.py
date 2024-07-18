"""Main telegram-bot logic & funcs."""

import os
import requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from selfcare.models import Person, PersonsHelpTips, PresetsHelpTips

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


class Command(BaseCommand):
    """Create custom django-admin commands."""

    help = 'Telegram bot for selfcare'

    def handle(self, *args, **options):
        """Make a bot and start work."""
        bot = TeleBot(token=BOT_TOKEN)

        @bot.message_handler(commands=['loadsets'])
        def load_presets(message):
            chat_id = message.chat.id
            name = message.chat.first_name

            person, _ = Person.objects.get_or_create(
                tlg_id=chat_id,
                defaults={
                    'name': name,
                }
            )
            helptips = PresetsHelpTips.objects.all()
            bulk_list = []
            for tip in helptips:
                bulk_list.append(
                    PersonsHelpTips(
                        text=tip.text,
                        person=person,
                        preset_tip=tip
                    )
                )
            PersonsHelpTips.objects.bulk_create(bulk_list)
            bot.send_message(chat_id, text='Presets loaded')

        @bot.message_handler(commands=['need_support'])
        def get_support(message):
            chat_id = message.chat.id
            # пока сделала так, чтобы рандомно, но нужно переделать
            text = PersonsHelpTips.objects.order_by('?').first()
            bot.send_message(chat_id, text=text)

        @bot.message_handler(commands=['start'])
        def wake_up(message):
            chat_id = message.chat.id
            chat = message.chat
            name = chat.first_name

            Person.objects.get_or_create(
                tlg_id=chat_id,
                defaults={
                    'name': name,
                }
            )
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_loadsets = types.KeyboardButton('/loadsets')
            button_getsupport = types.KeyboardButton('/need_support')
            button_moodtracker = types.KeyboardButton('/moodtracker')
            button_selfesteem = types.KeyboardButton('/selfesteem')
            keyboard.add(button_loadsets)
            keyboard.add(button_getsupport)
            keyboard.add(button_moodtracker)
            keyboard.add(button_selfesteem)

            bot.send_message(
                chat_id=chat.id,
                text=f'Привет, {name}! Воспользуйтесь меню:',
                reply_markup=keyboard,
            )

        bot.infinity_polling()
