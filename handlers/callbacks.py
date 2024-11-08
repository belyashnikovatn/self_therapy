from contextlib import suppress

from random import choice

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from db.operations import set_user, get_advices, add_note
import keyboards.menu as menu


router = Router()


class Mood(StatesGroup):
    """For mood tracking"""
    addition = State()
    finish = State()


class Selfesteem(StatesGroup):
    """For selfesteem tracking"""
    addition = State()
    finish = State()


@router.callback_query(F.data == 'get_data')
async def get_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await set_user(
        tg_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name
    )
    advices = await get_advices(
        user_id=user.id
    )
    # user_data = await state.get_data()
    await callback.message.answer(
        # text=f'Вот оно: {user_data.get("mood")}.\n'
        # f'{user_data.get("selfesteem")}',
        text=f'{user} \n'
        f'{advices}',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery):
    user = await set_user(
        tg_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name
    )
    await callback.message.answer(
        text=f'Хей {user} \n Выберите пункт меню:',
        reply_markup=menu.get_main_menu()
    )


@router.callback_query(F.data == 'support')
async def send_support(callback: CallbackQuery):
    advices = await get_advices(
        user_id=callback.from_user.id
    )
    await callback.message.answer(
        text=choice(advices).get('text'),
        reply_markup=menu.get_more_help()
    )


@router.callback_query(F.data == 'mood')
async def get_mood(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        'Напишите в любой форме, что вы сейчас чувствуете'
    )
    await state.set_state(Mood.addition)


@router.callback_query(F.data == 'selfesteem')
async def get_selfesteem(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Напишите, что у вас сегодня получилось сделать'
    )
    await state.set_state(Selfesteem.addition)


@router.callback_query(F.data == 'mood_diary')
async def get_all_mood(callback: CallbackQuery):
    await callback.message.answer(
        text='Скоро тут будут выводиться все записи \n'
        'дневника настроений',
        reply_markup=menu.get_main_menu()
    )


@router.callback_query(F.data == 'selfesteem_diary')
async def get_all_selfesteem(callback: CallbackQuery):
    await callback.message.answer(
        text='Скоро тут будут выводиться все записи \n'
        'дневника самооценки',
        reply_markup=menu.get_main_menu()
    )


@router.message(Mood.addition, F.text)
async def mood_done(message: Message, state: FSMContext):
    # await state.update_data(mood=message.text)
    # mood = await state.get_data()
    await add_note(
        user_id=message.from_user.id,
        type='mood',
        text=message.text
    )
    await message.answer(
        text=f'Данные сохранены',
        reply_markup=menu.after_mood()
    )
    await state.set_state(Mood.finish)


@router.message(Selfesteem.addition, F.text)
async def mood_done(message: Message, state: FSMContext):
    await state.update_data(selfesteem=message.text)
    await message.answer(
        text=f'Данные сохранены',
        reply_markup=menu.after_selfesteem()
    )
    await state.set_state(Selfesteem.finish)


@router.message(F.text)
async def mood_done(message: Message):
    await message.answer(
        text='Не совсем поянтно, что вы имеете в виду. \n'
        'Давайте начнём заново:',
        reply_markup=menu.get_main_menu()
    )
