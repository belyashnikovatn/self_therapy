from db.database import async_session, Base, engine


def connection(func):
    """Decorator for any DB connection."""
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


async def create_tables():
    """Create all the tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
