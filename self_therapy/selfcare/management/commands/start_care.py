"""Main telegram-bot logic & funcs."""

import os
import requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from selfcare.models import Person, PersonsHelpTips, PresetsHelpTips

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


class Command(BaseCommand):
    help = 'Telegram bot for selfcare'

    def handle(self, *args, **options):
        bot = TeleBot(token=BOT_TOKEN)

        @bot.message_handler(commands=['need_help'])
        def get_help(message):
            chat = message.chat
            text = PresetsHelpTips.objects.order_by('?').first()
            bot.send_message(chat.id, text=text)
        
        @bot.message_handler(commands=['start'])
        def wake_up(message):
            chat = message.chat
            name = chat.first_name
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_gethelp = types.KeyboardButton('/need_help')
            button_moodtracker = types.KeyboardButton('/moodtracker')
            button_selfesteem = types.KeyboardButton('/selfesteem')
            keyboard.add(button_gethelp)
            keyboard.add(button_moodtracker)
            keyboard.add(button_selfesteem)

            bot.send_message(
                chat_id=chat.id,
                text=f'Привет, {name}! Выбери пункт меню:',
                reply_markup=keyboard,
            )

        bot.infinity_polling()
