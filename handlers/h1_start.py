# handlers/h1_start.py
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from utils.auth import check_access, is_driver, is_admin
from keyboards.reply import reply_drive_menu, reply_admin_menu  # меню водителя и админа

router = Router()

@router.message(F.text == "/start")
async def h1_start(message: Message):
    """Приветственное меню с проверкой прав и выводом своей клавиатуры"""
    access = await check_access(message)
    if not access:
        return

    photo = FSInputFile("media/welcome.jpeg")

    if is_admin(message.from_user.id):
        await message.answer_photo(
            photo=photo,
            caption=f"Добро пожаловать, админ! <i>{message.from_user.full_name}</i>",
            parse_mode="HTML",
            reply_markup=reply_admin_menu()
        )
        return

    if is_driver(message.from_user.id):
        await message.answer_photo(
            photo=photo,
            caption=f"Добро пожаловать, водитель! <i>{message.from_user.full_name}</i>",
            parse_mode="HTML",
            reply_markup=reply_drive_menu()
        )
        return
