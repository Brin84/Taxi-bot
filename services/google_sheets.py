def add_record(user_id: int, username: str, record_type: str, subcategory: str, amount: float, comment: str):
    """Заглушка для записи в Google Sheets.
    Пока что просто выводим данные в консоль.
    """
    print(
        f"[GoogleSheetsStub] Запись добавлена:\n"
        f"Пользователь: {username} (ID: {user_id})\n"
        f"Тип: {record_type}\n"
        f"Подкатегория: {subcategory}\n"
        f"Сумма: {amount}\n"
        f"Комментарий: {comment}\n"
    )
