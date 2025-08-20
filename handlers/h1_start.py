from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_driver, is_admin
from keyboards.reply import reply_drive_menu, reply_admin_menu

router = Router()

@router.message(F.text == "/start")
async def h1_start(message: Message):
    """Приветственное меню с проверкой прав и выводом своей клавиатуры"""
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.answer(
            text="Добро пожаловать, админ!",
            reply_markup=reply_admin_menu()
        )
    elif is_driver(user_id):
        await message.answer(
            text="Добро пожаловать, водитель!",
            reply_markup=reply_drive_menu()
        )
    else:
        await message.answer(
            text="Обратитесь для работы с ботом к администратору."
        )
