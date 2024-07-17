"""Main telegram-bot logic & funcs."""

import os
from django.core.management.base import BaseCommand
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater
import requests
from telebot import TeleBot, types
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


class Command(BaseCommand):
    help = 'Telegram bot for selfcare'

    def handle(self, *args, **kwargs):
        bot = TeleBot(token=BOT_TOKEN)

        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text='HI',
        )
        bot.polling(none_stop=True)

