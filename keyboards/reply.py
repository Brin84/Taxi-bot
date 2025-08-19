from aiogram.utils.keyboard import ReplyKeyboardBuilder

def reply_drive_menu():
    """Главное меню водителя"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Доход")
    builder.button(text="➖ Расход")
    builder.button(text="📊 Отчёт")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)
