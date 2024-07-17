# """Main telegram-bot logic & funcs."""
# import os
# from dotenv import load_dotenv 
# from telebot import TeleBot, types
# from http import HTTPStatus
# import requests

# load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


# @bot.message_handler(commands=['start'])
# def wake_up(bot, message):
#     bot.send_message(
#         chat_id=TELEGRAM_CHAT_ID,
#         text=message,
#     )


# def main():
#     """Define main logic."""
#     bot = TeleBot(token=BOT_TOKEN)
#     bot.polling(none_stop=True)
#     wake_up(bot, 'hi')



# if __name__ == '__main__':
#     main()
