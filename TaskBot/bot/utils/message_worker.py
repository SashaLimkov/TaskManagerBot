import asyncio
import traceback

from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from bot.config.loader import bot
from bot.utils.deleter import try_delete_message


async def try_edit_message(
        message, user_id, text, main_message_id, keyboard, state: FSMContext
):
    """
    Функция, которая пытается обновить любое текстовое сообщение по main_message_id.
    :param message:
    :param user_id:
    :param text:
    :param main_message_id:
    :param keyboard:
    :param state:
    :return:
    """
    try:
        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            message_id=main_message_id,
            reply_markup=keyboard if keyboard else None,
        )
    except Exception:
        await try_send_message(message, user_id, text, keyboard, state)
        await try_delete_message(
            chat_id=user_id,
            message_id=main_message_id,
        )


async def try_send_voice(user_id, text, voice, keyboard, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    await try_delete_message(user_id, main_message_id)
    try:
        mes = await bot.send_voice(
            chat_id=user_id, voice=voice, caption=text, reply_markup=keyboard if keyboard else None
        )
        await state.update_data({"main_message_id": mes.message_id})
        return mes.message_id
    except Exception:
        print(traceback.format_exc())


async def try_send_message(message, user_id, text, keyboard, state: FSMContext):
    """Функция, которая пытается отправить любое текстовое сообщение.
    С учетом main_message_id для дальнейшего его обновления.
    Удаляет предыдущее главное сообщение.
    :param message:
    :param user_id:
    :param text:
    :param keyboard:
    :param state:
    :return:
    """
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    await try_delete_message(user_id, main_message_id)
    try:
        mes = await bot.send_message(
            chat_id=user_id, text=text, reply_markup=keyboard if keyboard else None
        )
        await state.update_data({"main_message_id": mes.message_id})
        return mes.message_id
    except Exception:
        print(traceback.format_exc())


async def try_edit_keyboard(
        chat_id: int,
        message_id: int,
        keyboard):
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
        )
    except:
        print(traceback.format_exc())


async def _spamer(chat_id: int, text: str):
    if chat_id:
        try:
            await bot.send_message(chat_id, text)
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)
            await _spamer(chat_id, text)
        except:
            print(traceback.format_exc())


async def spam_machine(text, chats):
    for chat in chats:
        await _spamer(chat.telegram_id, text)


async def dry_message_editor(text, keyboard, state, message):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    telegram_id = message.chat.id
    await try_edit_message(
        message=message,
        main_message_id=main_message_id,
        user_id=telegram_id,
        text=text,
        keyboard=keyboard,
        state=state
    )
