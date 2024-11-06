"""Required operations"""

from bot import logger
from db.base import connection
from db.models import User, Note
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id: int, username: str, full_name: str):
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f'User {tg_id} is registred')
            return None
        else:
            logger.info(f'User {tg_id} found!')
            return user
    except SQLAlchemyError as e:
        logger.error(f'Error!! {e}')
        await session.rollback()


