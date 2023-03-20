from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.services import telegram_user as user_services
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.states.MainMenu import MainMenu
from bot.states.Registration import UserRegistration
from bot.utils.message_worker import try_edit_message, try_send_message


async def start_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = td.REGISTRATION
    if main_message_id:
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )
    else:
        await try_send_message(
            message=message,
            user_id=user_id,
            text=text,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )


async def get_main_registration_menu(call: types.CallbackQuery, state: FSMContext):
    await get_registration_menu(message=call.message, state=state)


async def get_registration_menu(message: types.Message, state: FSMContext):
    await UserRegistration.MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = td.REGISTRATION_MAIN
    fio = data.get("fio", "")
    username = data.get("username", "")
    phone_number = data.get("phone_number", "")
    text = text.format(
        fio=fio,
        username=username,
        phone_number=phone_number,
    )
    if all((username, fio, phone_number)):
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            keyboard=await ik.get_user_registration_menu(done=True),
            main_message_id=main_message_id,
            state=state,
        )
        return
    await try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=await ik.get_user_registration_menu(),
        main_message_id=main_message_id,
        state=state,
    )


async def press_user_fio_or_phone(
        call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.from_user.id
    if callback_data["action"] == "1":
        await UserRegistration.FIO.set()
        text = td.REGISTRATION_FIO
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=0,
            state=state,
        )
    else:
        await UserRegistration.PHONE_NUMBER.set()
        text = td.REGISTRATION_NUMBER
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=await rk.get_phone_number(),
            state=state,
        )


async def get_user_fio(message: types.Message, state: FSMContext):
    username = message.chat.username
    await state.update_data({"fio": message.text, "username": username})
    await message.delete()
    await get_registration_menu(message=message, state=state)


async def get_user_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data({"phone_number": phone_number})
    await message.delete()
    await get_registration_menu(message=message, state=state)


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await MainMenu.MM.set()
    main_message_id = data.get("main_message_id", False)
    telegram_id = call.message.chat.id
    fio = data.get("fio", False)
    username = data.get("username", False)
    phone_number = data.get("phone_number", False)
    text = td.MAIN_MENU
    user_services.create_user(fio=fio, username=username, phone_number=phone_number, telegram_id=telegram_id)
    await try_edit_message(
        message=call.message,
        user_id=telegram_id,
        text=text,
        main_message_id=main_message_id,
        state=state,
        keyboard=await ik.get_main_menu()
    )
