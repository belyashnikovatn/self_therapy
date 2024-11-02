from contextlib import suppress

from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router()

support_tips = ['Дышите квадратами', 'Пробегитесь!', 'Умойтесь холодной водой']


@router.callback_query(F.data == 'support')
async def send_support(callback: CallbackQuery):
    await callback.message.answer(choice(support_tips))


@router.callback_query(F.data == 'mood')
async def get_mood(callback: CallbackQuery):
    await callback.message.answer('Как вы себя чувствуете?')


@router.callback_query(F.data == 'selfesteem')
async def get_selfesteem(callback: CallbackQuery):
    await callback.message.answer('Похвастайтесь как следует!')
