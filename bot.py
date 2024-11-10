import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

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

bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
admin = config.admin_token.get_secret_value()
