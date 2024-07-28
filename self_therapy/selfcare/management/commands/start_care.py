"""Main telegram-bot logic & funcs."""

import os
import requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from ...telegram_bot import TelegramBot

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


class Command(BaseCommand):
    """Create custom django-admin commands."""

    help = 'Telegram bot for selfcare'

    def handle(self, *args, **options):
        """Make a bot and start work."""

        bot = TelegramBot(token=BOT_TOKEN)
        bot.infinity_polling()
