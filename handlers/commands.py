from random import choice

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.operations import (
    add_note,
    get_advices,
    get_notes,
    set_user,
)
import keyboards.keyboards as kb


router = Router()


class Mood(StatesGroup):
    """For mood tracking"""
    addition = State()


class Selfesteem(StatesGroup):
    """For selfesteem tracking"""
    addition = State()


@router.message(F.text == '🏠 Главное меню')
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle start command"""
    await state.clear()
    user = await set_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
    await message.answer(
        f'{user.full_name}, давайте подумаем, чего вам хочется',
        reply_markup=kb.main_kb()
    )


@router.message(F.text == '❌ Отменить действие')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Действие отменено. Воспользуйтесь меню',
        reply_markup=kb.main_kb()
        )


@router.message(F.text.startswith('❤‍🩹'))
async def cmd_put_advice(message: Message, state: FSMContext):
    await state.clear()
    advices = await get_advices(
        user_id=message.from_user.id
    )
    await message.answer(
        text=choice(advices)['text'],
        reply_markup=kb.more_help()
    )


@router.message(F.text.startswith('👤'))
async def cmd_add_mood(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Напишите как можно подробнее, что вы сейчас чувствуете \n'
        'Помните, что нет плохих или хороших эмоций: все они важны. \n',
        reply_markup=kb.stop_fsm()
    )
    await state.set_state(Mood.addition)


@router.message(Mood.addition, F.text)
async def cmd_mood_done(message: Message, state: FSMContext):
    await add_note(
        user_id=message.from_user.id,
        type='mood',
        text=message.text
    )
    await message.answer(
        text='Спасибо, что поделились',
        reply_markup=kb.mood()
    )
    await state.clear()


@router.message(F.text.startswith('💌'))
async def cmd_selfesteem_add(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Вспомните, что полезного/приятного/хорошего вы'
        'сегодня сделали. Это может быть что угодно, но важно, '
        'что вы об этом ещё никому не сказали. Напишите одну вещь.',
        reply_markup=kb.stop_fsm()
    )
    await state.set_state(Selfesteem.addition)


@router.message(Selfesteem.addition, F.text)
async def cmd_selfesteem_done(message: Message, state: FSMContext):
    await add_note(
        user_id=message.from_user.id,
        type='selfesteem',
        text=message.text
    )
    await message.answer(
        text='Отлично!',
        reply_markup=kb.selfesteem()
    )
    await state.clear()


@router.message(F.text == '🗒 Дневник эмоций')
async def cmd_get_mood(message: Message, state: FSMContext):
    await state.clear()
    moods = await get_notes(
        user_id=message.from_user.id,
        type='mood'
    )
    if moods:
        text = '\n'.join([mood['text'] for mood in moods])
    else:
        text = 'Пока что нет ни одной строчки'
    await message.answer(
        text=text,
        reply_markup=kb.main_kb()
    )


@router.message(F.text == '🗒 Дневник самооценки')
async def cmd_get_selfesteem(message: Message, state: FSMContext):
    await state.clear()
    selfesteems = await get_notes(
        user_id=message.from_user.id,
        type='selfesteem'
    )
    if selfesteems:
        text = '\n'.join([selfesteem['text'] for selfesteem in selfesteems])
    else:
        text = 'Пока что нет ни одной стрчоки'
    await message.answer(
        text=text,
        reply_markup=kb.main_kb()
    )



@router.callback_query(F.data == 'main_menu')
async def main_menu_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    await call.message.answer(
        'Выберите необходимое действие',
        reply_markup=kb.main_kb()
    )
