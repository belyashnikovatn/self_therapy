# import asyncio
# from keyboards.keyboards import manage_note

# import ..bot


# async def send_count_notes(notes, bot, user_id):
#     for note in notes:
#         try:
#             await bot.send_message(
#                 bot=bot,
#                 text=note['text'],
#                 user_id=user_id,
#                 reply_markup=manage_note(note['id'])
#             )
#         except Exception as e:
#             # logger.error(f'Ошибка: смотри {e}')
#             await asyncio.sleep(2)
#         finally:
#             await asyncio.sleep(0.5)
