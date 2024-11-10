from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from constants import NOTES_COUNT
from db.operations import (
    add_note,
    delete_note,
    get_note,
    get_notes,
    update_note
)
from keyboards import (
    kb_main_menu,
    kb_notes
)

router = Router()


class AddMood(StatesGroup):
    """For mood tracking"""
    progress = State()


class AddSelfesteem(StatesGroup):
    """For selfesteem tracking"""
    progress = State()


class EditNote(StatesGroup):
    """For any note tracking"""
    progress = State()


@router.message(F.text.startswith('🎉'))
@router.message(F.text.startswith('👤'))
async def cmd_pre_post(message: Message, state: FSMContext):
    """Add into diary emotion/selfesteem: first step."""
    await state.clear()
    if message.text.startswith('🎉'):
        text = ('Вспомните, что полезного/приятного/хорошего вы '
        'сегодня сделали. Это может быть что угодно, но важно, '
        'что вы об этом ещё никому не сказали. Напишите одну вещь.')
        await state.set_state(AddSelfesteem.progress)
    elif message.text.startswith('👤'):
        text = ('Напишите как можно подробнее, что вы сейчас чувствуете \n'
        'Помните, что нет плохих или хороших эмоций: все они важны. \n')
        await state.set_state(AddMood.progress)
    await message.answer(
        text=text,
        reply_markup=kb_main_menu.stop_fsm()
    )


@router.message(AddMood.progress, F.text)
async def cmd_mood_post(message: Message, state: FSMContext):
    """Add an emotion: second last step."""
    await add_note(
        user_id=message.from_user.id,
        type='mood',
        text=message.text
    )
    await message.answer(
        text='Спасибо, что поделились',
        reply_markup=kb_notes.mood()
    )
    await state.clear()


@router.message(AddSelfesteem.progress, F.text)
async def cmd_selfesteem_post(message: Message, state: FSMContext):
    """Add a selfesteem: second last step."""
    await add_note(
        user_id=message.from_user.id,
        type='selfesteem',
        text=message.text
    )
    await message.answer(
        text='Отлично!',
        reply_markup=kb_notes.selfesteem()
    )
    await state.clear()


@router.message(F.text.startswith('🗒 Дневник'))
async def cmd_notes_get(message: Message, state: FSMContext):
    """Get diary by type: emotions or selfesteem."""
    await state.clear()
    type = message.text.split(' ')[-1]
    if  type == 'эмоций':
        type = 'mood'
    elif type == 'самооценки':
        type = 'selfesteem'

    notes = await get_notes(
        user_id=message.from_user.id,
        type=type,
        count=NOTES_COUNT
    )
    if notes:
        await message.answer(
            'Записи ниже в списке. Выберите нужную',
            reply_markup=kb_notes.notes_list(notes))
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )


@router.callback_query(F.data.startswith('manage_note_'))
async def cmd_note_get(call: CallbackQuery, state: FSMContext):
    """Get a note of any type to edit or delete."""
    await call.answer()
    await state.clear()
    note_id = int(call.data.replace('manage_note_', ''))
    note = await get_note(note_id=note_id)
    await call.message.answer(
        text=f'Вот запись {note["text"]}',
        reply_markup=kb_notes.manage_note(note_id)
        )


@router.callback_query(F.data.startswith('edit_note_'))
async def cmd_note_pre_put(call: CallbackQuery, state: FSMContext):
    """Editing text from any note by id: first step."""
    await state.clear()
    note_id = int(call.data.replace('edit_note_', ''))
    await call.answer(f'Редактируем текст {note_id}')
    await state.update_data(note_id=note_id)
    await call.message.answer(f'Отправьте новый текст {note_id}')
    await state.set_state(EditNote.progress)


@router.message(EditNote.progress, F.text)
async def cmd_note_put(message: Message, state: FSMContext):
    """Editing text from any note by id: last step."""
    note_data = await state.get_data()
    note_id = note_data['note_id']
    note = await get_note(note_id=note_id)

    text = message.text.strip()
    await update_note(
        note_id=note_id,
        text=text
    )
    await state.clear()

    notes = await get_notes(
        user_id=message.from_user.id,
        type=note['type'],
        count=NOTES_COUNT
    )
    if notes:
        await message.answer(
            text='Запись изменена!',
            reply_markup=kb.notes_list(notes)
        )
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )


@router.callback_query(F.data.startswith('delete_note_'))
async def cmd_note_delete(call: CallbackQuery, state: FSMContext):
    """Delete any note by id."""
    await state.clear()
    note_id = int(call.data.replace('delete_note_', ''))
    note = await get_note(note_id=note_id)
    await delete_note(note_id=note_id)
    await call.answer(
        text=f'Запись номер {note_id} удалена',
        show_alert=True,
    )
    await call.message.delete()

    notes = await get_notes(
        user_id=call.from_user.id,
        type=note['type'],
        count=NOTES_COUNT
    )
    if notes:
        await call.message.answer(
            text='Записи ниже в списке. Выберите нужную',
            reply_markup=kb_notes.notes_list(notes)
        )
    else:
        await call.message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb_main_menu.main_kb()
        )
