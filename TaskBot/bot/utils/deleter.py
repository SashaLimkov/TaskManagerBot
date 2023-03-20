import traceback

from bot.config.loader import bot


async def try_delete_message(chat_id: str | int, message_id: str | int | list):
    try:
        if type(message_id) != list:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        elif type(message_id) == list:
            for mes_id in message_id:
                await try_delete_message(chat_id, mes_id)
    except Exception as e:
        print(message_id)
        print(e)
