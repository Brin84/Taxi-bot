from aiogram.utils.keyboard import ReplyKeyboardBuilder

def reply_drive_menu():
    """Главное меню для водителя"""
    kb = ReplyKeyboardBuilder()
    kb.button(text="➕ Добавить доход")
    kb.button(text="➖ Добавить расход")
    kb.button(text="📊 Отчёт")
    kb.adjust(1, 2)
    return kb.as_markup(resize_keyboard=True)

