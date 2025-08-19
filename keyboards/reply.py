from aiogram.utils.keyboard import ReplyKeyboardBuilder

def reply_drive_menu():
    """Клавиатура для водителя"""
    build = ReplyKeyboardBuilder()
    build.button(text="Добавить доход 💰")
    build.button(text="Добавить расход 🧾")
    build.button(text="Отчёт 📊")
    build.adjust(1, 3)
    return build.as_markup(resize_keyboard=True)

def reply_admin_menu():
    """Клавиатура для администратора"""
    build = ReplyKeyboardBuilder()
    build.button(text="Сводка по водителям 📑")
    build.button(text="Добавить водителя ➕")
    build.button(text="Удалить водителя ❌")
    build.button(text="Экспорт данных 📤")
    build.button(text="Настройки ⚙")
    build.adjust(1, 3)
    return build.as_markup(resize_keyboard=True)

def income_menu():
    """Клавиатура для меню дохода водителя"""
    build = ReplyKeyboardBuilder()
    build.button(text="Добавить наличные 💵")
    build.button(text="Добавить безнал 🏦")
    build.button(text="Назад 🔙")
    build.adjust(1, 2)
    return build.as_markup(resize_keyboard=True)
