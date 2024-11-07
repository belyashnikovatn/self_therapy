"""Required operations"""

from bot import logger
from db.base import connection
from db.models import User, Note, Advice
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


help_advices = [
    'Дышите квадратами', 'Пробегитесь!', 'Умойтесь холодной водой', 'Catttsss'
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
        logger.error(f'Ошибка! Смотри {e}')
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
        logger.error(f'Ошибка! Смотри {e}')
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
        logger.error(f'Ошибка! Смотри {e}')
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
            'text': note.text
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка! Смотри {e}')
        return None
