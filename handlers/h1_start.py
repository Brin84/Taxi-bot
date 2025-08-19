from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from keyboards.reply import reply_drive_menu
from utils.auth import is_driver, is_admin

router = Router()


@router.message(F.text == "/start")
async def h1_start(message: Message):
    """Приветственное меню и меню водителя/админа"""
    photo = FSInputFile("media/welcome.jpeg")


    if is_admin(message.from_user.id):
        text = f"Добро пожаловать, админ! <i>{message.from_user.full_name}</i>"

        await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")
        return

    if is_driver(message.from_user.id):
        text = f"Добро пожаловать, водитель! <i>{message.from_user.full_name}</i>"
        await message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode="HTML",
            reply_markup=reply_drive_menu()
        )
        return

    await message.answer("❌ У вас нет доступа к боту.")
