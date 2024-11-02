from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.menu import get_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle start command"""
    await message.answer(
        'Выберите пункт меню:',
        reply_markup=get_main_menu()
    )