import json
from config import ADMINS_FILE, MAIN_ADMIN, DRIVERS
import os


def _load_admins():
    """Загрузить список администраторов из файла"""
    if not os.path.exists(ADMINS_FILE):
        os.makedirs(os.path.dirname(ADMINS_FILE), exist_ok=True)
        with open(ADMINS_FILE, "w", encoding="utf-8") as f:
            json.dump([MAIN_ADMIN], f, ensure_ascii=False, indent=2)
    with open(ADMINS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = [MAIN_ADMIN]

    if isinstance(data, list):
        return data
    return [MAIN_ADMIN]

def _save_admins(admins_list):
    """Сохранить список администраторов в файл"""
    with open(ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump(admins_list, f, ensure_ascii=False, indent=2)


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in _load_admins()

def is_main_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь главным администратором"""
    return user_id == MAIN_ADMIN


def add_admin(user_id: int) -> bool:
    """Добавить администратора (кроме уже существующих)"""
    admins = _load_admins()
    if user_id in admins:
        return False
    admins.append(user_id)
    _save_admins(admins)
    return True

def remove_admin(user_id: int) -> bool:
    """Удалить администратора (кроме главного)"""
    if user_id == MAIN_ADMIN:
        return False
    admins = _load_admins()
    if user_id in admins:
        admins.remove(user_id)
        _save_admins(admins)
        return True
    return False

def get_all_admins():
    """Вернуть список всех администраторов"""
    return _load_admins()


def is_driver(user_id: int) -> bool:
    """Проверка, является ли пользователь водителем"""
    return user_id in DRIVERS
