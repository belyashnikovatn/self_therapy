import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config


def init_logger():
    """Customize logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s, [%(levelname)s], %(message)s, %(funcName)s'
    )
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger


logger = init_logger()


async def main():
    dp = Dispatcher()
    bot = Bot(token=config.bot_token.get_secret_value())
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logger.info('Exit')