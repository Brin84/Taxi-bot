from config import ADMINS, DRIVERS
from aiogram.types import Message

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMINS

def is_driver(user_id: int) -> bool:
    """Проверка, является ли пользователь водителем"""
    return user_id in DRIVERS

async def check_access(message: Message) -> bool:
    """Проверка доступа пользователя при входе в бот."""
    user_id = message.from_user.id
    if is_admin(user_id) or is_driver(user_id):
        return True
    await message.answer("❌ У вас нет доступа к боту.")
    return False
