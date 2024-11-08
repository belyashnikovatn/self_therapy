from random import choice

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from db.operations import (
    add_note,
    delete_note,
    get_advices,
    get_note,
    get_notes,
    set_user,
    update_note
)
import keyboards.keyboards as kb

router = Router()


class AddMood(StatesGroup):
    """For mood tracking"""
    progress = State()


class AddSelfesteem(StatesGroup):
    """For selfesteem tracking"""
    progress = State()


class EditNote(StatesGroup):
    """For mood tracking"""
    progress = State()


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
async def cmd_advice_get(message: Message, state: FSMContext):
    await state.clear()
    advices = await get_advices(
        user_id=message.from_user.id
    )
    await message.answer(
        text=choice(advices)['text'],
        reply_markup=kb.more_help()
    )


@router.message(F.text.startswith('👤'))
async def cmd_mood_pre_post(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Напишите как можно подробнее, что вы сейчас чувствуете \n'
        'Помните, что нет плохих или хороших эмоций: все они важны. \n',
        reply_markup=kb.stop_fsm()
    )
    await state.set_state(AddMood.progress)


@router.message(AddMood.progress, F.text)
async def cmd_mood_post(message: Message, state: FSMContext):
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
async def cmd_selfesteem_pre_post(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Вспомните, что полезного/приятного/хорошего вы'
        'сегодня сделали. Это может быть что угодно, но важно, '
        'что вы об этом ещё никому не сказали. Напишите одну вещь.',
        reply_markup=kb.stop_fsm()
    )
    await state.set_state(Selfesteem.addition)


@router.message(AddSelfesteem.progress, F.text)
async def cmd_selfesteem_post(message: Message, state: FSMContext):
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
async def cmd_moods_get(message: Message, state: FSMContext):
    await state.clear()
    moods = await get_notes(
        user_id=message.from_user.id,
        type='mood'
    )
    if moods:
        # text = '\n'.join([mood['text'] for mood in moods])
        await message.answer(
            'Записи ниже в списке. Выберите нужную',
            reply_markup=kb.short_texts_notes(moods))
    else:
        await message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb.main_kb()
        )


@router.message(F.text == '🗒 Дневник самооценки')
async def cmd_selfesteems_get(message: Message, state: FSMContext):
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


@router.message(F.text == '⚙ Настройки')
async def cmd_sets_get(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Выберите необходимое действие',
        reply_markup=kb.get_sets()
    )


@router.callback_query(F.data == 'main_menu')
async def cmd_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    await call.message.answer(
        'Выберите необходимое действие',
        reply_markup=kb.main_kb()
    )


@router.callback_query(F.data.startswith('manage_note_'))
async def cmd_note_get(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    note_id = int(call.data.replace('manage_note_', ''))
    note = await get_note(note_id=note_id)
    await call.message.answer(
        text=f'Вот запись {note["text"]}',
        # text=f'{note_id}',
        reply_markup=kb.manage_note(note_id)
        )


@router.callback_query(F.data.startswith('edit_note_'))
async def cmd_note_pre_put(call: CallbackQuery, state: FSMContext):
    await state.clear()
    note_id = int(call.data.replace('edit_note_', ''))
    await call.answer(f'Редактируем текст {note_id}')
    await state.update_data(note_id=note_id)
    await call.message.answer(f'Отправьте новый текст {note_id}')
    await state.set_state(EditNote.progress)


@router.message(EditNote.progress, F.text)
async def cmd_note_put(message: Message, state: FSMContext):
    note_data = await state.get_data()
    note_id = note_data['note_id']
    text = message.text.strip()
    await update_note(
        note_id=note_id,
        text=text
    )
    await state.clear()
    await message.answer(
        text='Запись изменена',
        reply_markup=kb.main_kb()
    )
    await state.clear()


@router.callback_query(F.data.startswith('delete_note_'))
async def cmd_note_delete(call: CallbackQuery, state: FSMContext):
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
        type=note['type']
    )
    if notes:
        await call.message.answer(
            'Записи ниже в списке. Выберите нужную',
            reply_markup=kb.short_texts_notes(notes)
        )
    else:
        await call.message.answer(
            text='Пока что нет ни одной строчки',
            reply_markup=kb.main_kb()
        )
