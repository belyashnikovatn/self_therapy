from random import choice

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from constants import ADVICES_COUNT
from db.operations import (
    get_advice,
    delete_advice,
    get_advices,
    update_advice
)
from keyboards import (
    kb_advices,
    kb_main_menu,
)

router = Router()


class AddAdvice(StatesGroup):
    """For advice tracking"""
    progress = State()


class EditAdvice(StatesGroup):
    """For advice tracking"""
    progress = State()


@router.message(F.text.startswith('💔'))
async def cmd_advice_get(message: Message, state: FSMContext):
    """Get 1 of all help advices"""
    await state.clear()
    advices = await get_advices(
        user_id=message.from_user.id
    )
    await message.answer(
        text=choice(advices)['text'],
        reply_markup=kb_advices.advice()
    )


@router.message(F.text.startswith('❤ Список'))
async def cmd_advices_get(message: Message, state: FSMContext):
    await state.clear()
    advices = await get_advices(
        user_id=message.from_user.id
    )
    if advices:
        await message.answer(
            'Записи ниже в списке. Выберите нужную',
            reply_markup=kb_advices.advices_list(advices))
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )


@router.callback_query(F.data.startswith('manage_advice_'))
async def cmd_advice_get_to_change(call: CallbackQuery, state: FSMContext):
    """Get an advice to edit or delete."""
    await call.answer()
    await state.clear()
    advice_id = int(call.data.replace('manage_advice_', ''))
    advice = await get_advice(advice_id=advice_id)
    await call.message.answer(
        text=f'Вот запись {advice["text"]}',
        # text=f'{note_id}',
        reply_markup=kb_advices.manage_advice(advice_id)
        )


@router.callback_query(F.data.startswith('edit_advice_'))
async def cmd_advice_pre_put(call: CallbackQuery, state: FSMContext):
    """Editing text of advice by id: first step."""
    await state.clear()
    advice_id = int(call.data.replace('edit_advice_', ''))
    await call.answer(f'Редактируем текст {advice_id}')
    await state.update_data(advice_id=advice_id)
    await call.message.answer(f'Отправьте новый текст {advice_id}')
    await state.set_state(EditAdvice.progress)


@router.message(EditAdvice.progress, F.text)
async def cmd_advice_put(message: Message, state: FSMContext):
    """Editing text of advice by id: last step."""
    advice_data = await state.get_data()
    advice_id = advice_data['id']

    text = message.text.strip()
    await update_advice(
        advice_id=advice_id,
        text=text
    )
    await state.clear()

    # Output a list of advices after editing.
    advices = await get_advices(
        user_id=message.from_user.id,
        count=ADVICES_COUNT
    )
    if advices:
        await message.answer(
            text='Запись изменена!',
            reply_markup=kb_advices.advices_list(advices)
        )
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )


@router.callback_query(F.data.startswith('delete_advice_'))
async def cmd_advice_delete(call: CallbackQuery, state: FSMContext):
    """Delete advice by id."""
    await state.clear()
    advice_id = int(call.data.replace('delete_advice_', ''))
    await delete_advice(advice_id=advice_id)
    await call.answer(
        text=f'Запись номер {advice_id} удалена',
        show_alert=True,
    )
    await call.message.delete()

    # Output a list of advices after deleting.
    advices = await get_advices(
        user_id=message.from_user.id,
        count=ADVICES_COUNT
    )
    if advices:
        await message.answer(
            text='Запись изменена!',
            reply_markup=kb_advices.advices_list(advices)
        )
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )
