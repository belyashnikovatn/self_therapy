from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.operations import (
    get_statistic,
    set_user
)
from keyboards import (
    kb_main_menu,
)

router = Router()


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
        reply_markup=kb_main_menu.main_kb()
    )


@router.message(F.text == '⭐ Как это работает')
async def cmd_cancel(message: Message, state: FSMContext):
    """Documentation"""
    await state.clear()
    await message.answer(
        'Обычная магия, ничего такого',
        reply_markup=kb_main_menu.main_kb()
        )


@router.message(F.text == '❌ Отменить действие')
async def cmd_cancel(message: Message, state: FSMContext):
    """Cancel any action"""
    await state.clear()
    await message.answer(
        'Действие отменено. Воспользуйтесь меню',
        reply_markup=kb_main_menu.main_kb()
        )


@router.message(F.text == '⚙ Настройки')
async def cmd_sets_get(message: Message, state: FSMContext):
    """Gets all sets"""
    await state.clear()
    await message.answer(
        text='Выберите необходимое действие',
        reply_markup=kb_main_menu.get_sets()
    )


@router.message(F.text == '📊 Статистика')
async def cmd_statistic_get(message: Message, state: FSMContext):
    """Get statistic"""
    await state.clear()
    results = await get_statistic(
        user_id=message.from_user.id
    )
    await message.answer(
        f'На сегодня: {results}',
        reply_markup=kb_main_menu.main_kb()
        )


@router.callback_query(F.data == 'main_menu')
async def cmd_main_menu(call: CallbackQuery, state: FSMContext):
    """Come back to Main menu from note editing mode."""
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    await call.message.answer(
        'Выберите необходимое действие',
        reply_markup=kb_main_menu.main_kb()
    )
