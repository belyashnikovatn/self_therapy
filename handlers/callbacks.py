from contextlib import suppress

from random import choice

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import CallbackQuery

from keyboards.menu import get_main_menu


router = Router()

support_tips = ['Дышите квадратами', 'Пробегитесь!', 'Умойтесь холодной водой']


class AddDiary(StatesGroup):
    addition_mood = State()
    addition_selfesteem = State()
    finish = State()


@router.callback_query(F.data == 'get_data')
async def send_support(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.answer(
        text=f'Вот оно: {user_data["mood"]}.\n'
        f'{user_data["selfesteem"]}',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.callback_query(F.data == 'support')
async def send_support(callback: CallbackQuery):
    await callback.message.answer(choice(support_tips))


@router.callback_query(F.data == 'mood')
async def get_mood(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Как вы себя чувствуете?')
    await state.set_state(AddDiary.addition_mood)


@router.callback_query(F.data == 'selfesteem')
async def get_selfesteem(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Похвастайтесь как следует!')
    await state.set_state(AddDiary.addition_selfesteem)


@router.message(AddDiary.addition_mood, F.text)
async def mood_done(message: Message, state: FSMContext):
    await state.update_data(mood=message.text)
    await message.answer(
        text=f'Настроение сохранено'
    )
    await state.set_state(AddDiary.finish)


@router.message(AddDiary.addition_selfesteem, F.text)
async def mood_done(message: Message, state: FSMContext):
    await state.update_data(selfesteem=message.text)
    await message.answer(
        text=f'Похвала сохранена'
    )
    await state.set_state(AddDiary.finish)


@router.message(F.text)
async def mood_done(message: Message, state: FSMContext):
    await message.answer(
        text='Происходит что-то непонятное',
        reply_markup=get_main_menu()
    )
