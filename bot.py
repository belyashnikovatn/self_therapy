import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from config_reader import config
from handlers import (
    advices_cmds,
    main_cmds,
    notes_cmds,
)
from db.base import create_tables


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
    bot = Bot(token=config.bot_token.get_secret_value())
    start_cmds = [BotCommand(command='start', description='Начало')]
    await bot.set_my_commands(start_cmds, BotCommandScopeDefault())
    dp = Dispatcher()
    await create_tables()
    dp.include_router(main_cmds.router)
    dp.include_router(advices_cmds.router)
    dp.include_router(notes_cmds.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logger.info('Exit')
