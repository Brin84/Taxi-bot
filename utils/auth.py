from config import ADMIN, DRIVERS

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id == ADMIN

def is_driver(user_id: int) -> bool:
    """Проверка, является ли пользователь водителем"""
    return user_id in DRIVERS

