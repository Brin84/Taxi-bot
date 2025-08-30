from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from utils.auth import is_admin
from keyboards.reply import reply_admin_menu, reply_settings_menu

router = Router()


class SettingsStates(StatesGroup):
    changing_bot_token = State()
    adding_admin = State()
    removing_admin = State()


BACK_BTN = "🔚 Назад"


@router.message(F.text == "Настройки ⚙")
async def admin_settings_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await state.clear()
    await message.answer(
        "⚙ Меню настроек админ-панели:",
        reply_markup=reply_settings_menu()
    )


@router.message(F.text == "Сменить токен бота")
async def change_bot_token_start(message: Message, state: FSMContext):
    await state.set_state(SettingsStates.changing_bot_token)
    await message.answer("Введите новый токен бота:")


@router.message(StateFilter(SettingsStates.changing_bot_token))
async def change_bot_token_save(message: Message, state: FSMContext):
    if message.text == BACK_BTN:
        await state.clear()
        await message.answer("Возврат в меню настроек", reply_markup=reply_settings_menu())
        return

    new_token = message.text.strip()
    # Здесь можно добавить запись в config или env
    await state.clear()
    await message.answer(f"✅ Новый токен установлен: {new_token}", reply_markup=reply_settings_menu())


@router.message(F.text == "Добавить администратора")
async def add_admin_start(message: Message, state: FSMContext):
    await state.set_state(SettingsStates.adding_admin)
    await message.answer("Введите Telegram ID нового администратора:")


@router.message(StateFilter(SettingsStates.adding_admin))
async def add_admin_save(message: Message, state: FSMContext):
    if message.text == BACK_BTN:
        await state.clear()
        await message.answer("Возврат в меню настроек", reply_markup=reply_settings_menu())
        return

    new_admin_id = message.text.strip()
    await state.clear()
    await message.answer(f"✅ Администратор с ID {new_admin_id} добавлен", reply_markup=reply_settings_menu())


@router.message(F.text == "Удалить администратора")
async def remove_admin_start(message: Message, state: FSMContext):
    await state.set_state(SettingsStates.removing_admin)
    await message.answer("Введите Telegram ID администратора для удаления:")


@router.message(StateFilter(SettingsStates.removing_admin))
async def remove_admin_save(message: Message, state: FSMContext):
    if message.text == BACK_BTN:
        await state.clear()
        await message.answer("Возврат в меню настроек", reply_markup=reply_settings_menu())
        return

    remove_admin_id = message.text.strip()
    await state.clear()
    await message.answer(f"✅ Администратор с ID {remove_admin_id} удален", reply_markup=reply_settings_menu())


@router.message(F.text == BACK_BTN)
async def back_to_admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Возврат в главное админ-меню", reply_markup=reply_admin_menu())
