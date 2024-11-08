"""Required operations"""

from bot import logger
from db.base import connection
from db.models import User, Note, Advice
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


help_advices = [
    'Дыхание по квадрату: 4 секунды вдох, 4 секунды задержка, 4 секунды выдох, 4 секунды задержка.',
    'Найдите и обратите внимание:\r\n5. на ПЯТЬ «вещей», которые видите вокруг себя,\r\n4. на ЧЕТЫРЕ «вещи», которые можно потрогать, пощупать,\r\n3. на ТРИ вещи, которые вы можете слышать,\r\n2. на ДВЕ вещи, которые вы чувствуете по запаху,\r\n1. на ОДНУ вещь, которую вы можете попробовать.',
    'Возьмите ручку, лист бумаги и напишите: «Я сейчас чувствую...» А дальше пишите все, что приходит вам в голову — все чувства, мысли, эмоции, идеи и желания. Пишите до того момента, пока в голове не останется приятная пустота и спокойствие.',
    'Во время этого упражнения нужно попеременно напрягать и расслаблять мышцы. Сядьте прямо – так, чтобы спина касалась стула, ноги стояли на полу, а руки лежали на коленях. Начните с мышц кисти. Медленно считая до 5, с каждым счетом увеличивайте напряжение в мышцах кисти. На счет 5 резко расслабьте мышцы кисти. Теперь повторите это упражнение, напрягая не только мышцы кисти, но и мышцы предплечья. Затем подключите мышцы плеча, затем мышцы предплечья, далее мышцы плеча. В конце упражнения вы будете напрягать все мышцы рук и мышцы спины.'
]


@connection
async def set_user(session, tg_id, username, full_name):
    """Create a user and add all help advices."""
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f'Пользователь {tg_id} зареган')

            new_advices = [
                Advice(
                    text=item, user=new_user, rating=1.0
                ) for item in help_advices
            ]
            session.add_all(new_advices)

            await session.commit()
            logger.info(f'Базовые советы для {tg_id} добавлены')

            return user
        else:
            logger.info(f'Пользователь {tg_id} найден')
            return user
    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        await session.rollback()


@connection
async def get_advices(session, user_id):
    """Get all help advices by user."""
    try:
        result = await session.execute(select(Advice).filter_by(user_id=user_id))
        advices = result.scalars().all()

        if not advices:
            logger.info(f'У юзера {user_id} нет советов')
            return []

        advices_list = [
            {
                'id': advice.id,
                'text': advice.text,
                'rating': advice.rating
            } for advice in advices
        ]
        return advices_list

    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        return []


@connection
async def add_note(session, user_id, type, text):
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f'Пользователь с {id} не найден')
            return None
        new_note = Note(
            user_id=user_id,
            text=text,
            type=type,
        )
        session.add(new_note)
        await session.commit()
        logger.info(f'Запись типа {type} у {user_id} добавлена')
        return new_note
    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        await session.rollback()


@connection
async def get_note(session, note_id):
    try:
        note = await session.get(Note, note_id)
        if not note:
            logger.info(f'Запись с {note_id} не найдена')
            return None
        return {
            'id': note.id,
            'text': note.text,
            'date_created': note.created_at,
            'type': note.type
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        return None


@connection
async def get_notes(session, user_id, type):
    """Get mood or selfesteem notes by user."""
    try:
        result = await session.execute(select(Note).filter_by(
            user_id=user_id,
            type=type
        ))
        notes = result.scalars().all()

        if not notes:
            logger.info(f'Дневник юзера {user_id} пуст')
            return []

        notes_list = [
            {
                'id': note.id,
                'text': note.text,
                'date_created': note.created_at,
                'type': note.type
            } for note in notes
        ]
        return notes_list

    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        return []


@connection
async def update_note(session, note_id, text):
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))
        if not note:
            logger.error(f'Заметка {note_id} не найдена')
            return None

        note.text = text
        await session.commit()
        logger.info(f'Заметка {note_id} обновлена')
        return note
    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        await session.rollback()


@connection
async def delete_note(session, note_id):
    try:
        note = await session.get(Note, note_id)
        if not note:
            logger.error(f'Заметка {note_id} не найдена')
            return None
        await session.delete(note)
        await session.commit()
        logger.info(f'Заметка {note_id} удалена')
        return note
    except SQLAlchemyError as e:
        logger.error(f'Ошибка: смотри {e}')
        session.rollback()
        return None
