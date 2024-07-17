"""Main telegram-bot logic & funcs."""
import os
from dotenv import load_dotenv 
from telebot import TeleBot
from http import HTTPStatus

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')



def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
