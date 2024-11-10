import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from bot import bot, dp, logger, admin
from db.base import create_tables
from handlers import (
    advices_cmds,
    main_cmds,
    notes_cmds,
)


async def start_bot():
    start_cmds = [BotCommand(command='start', description='Начало')]
    await bot.set_my_commands(start_cmds, BotCommandScopeDefault())
    await create_tables()
    try:
        await bot.send_message(admin, 'Я запущен🥳')
    except:
        logger.error('Something goes ne tak')


async def stop_bot():
    try:
        await bot.send_message(admin, 'Its DONE!')
    except:
        logger.error('Something goes ne tak')


async def main():
    dp.include_router(main_cmds.router)
    dp.include_router(advices_cmds.router)
    dp.include_router(notes_cmds.router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logger.info('Exit')
