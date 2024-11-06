"""Required operations"""

from bot import logger
from db.base import connection
from db.models import User, Note
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id, username, full_name):
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f'Пользователь {tg_id} зареган')
            return None
        else:
            logger.info(f'Пользователь {tg_id} найден')
            return user
    except SQLAlchemyError as e:
        logger.error(f'Ошибка! Смотри {e}')
        await session.rollback()


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
