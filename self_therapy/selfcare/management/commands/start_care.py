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

        @bot.message_handler(commands=['need_support'])
        def get_support(message):
            chat = message.chat
            # пока сделала так, чтобы рандомно, но нужно переделать
            text = PresetsHelpTips.objects.order_by('?').first()
            bot.send_message(chat.id, text=text)

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
            button_getsupport = types.KeyboardButton('/need_support')
            button_moodtracker = types.KeyboardButton('/moodtracker')
            button_selfesteem = types.KeyboardButton('/selfesteem')
            keyboard.add(button_getsupport)
            keyboard.add(button_moodtracker)
            keyboard.add(button_selfesteem)

            bot.send_message(
                chat_id=chat.id,
                text=f'Привет, {name}! Выбери пункт меню:',
                reply_markup=keyboard,
            )

        bot.infinity_polling()
