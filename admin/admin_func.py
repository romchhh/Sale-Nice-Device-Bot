import os
import sqlite3
from openpyxl import Workbook
from aiogram import types

# Функція експорту конкретної таблиці до файлу Excel
def export_table_to_excel(table_name, file_name):
    conn = sqlite3.connect("db/data.db")
    c = conn.cursor()

    # Отримати всі дані з таблиці
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    # Створення нового файлу Excel
    wb = Workbook()
    ws = wb.active

    # Отримати назви стовпців
    c.execute(f"PRAGMA table_info({table_name})")
    column_names = [column[1] for column in c.fetchall()]

    # Запис назв стовпців у перший рядок файлу Excel
    ws.append(column_names)

    # Запис даних у файл Excel
    for row in rows:
        ws.append(row)

    # Збереження файлу Excel
    wb.save(file_name)

# Функція експорту бази даних до файлу Excel
async def export_database_to_excel(message: types.Message):
    # Експорт таблиці users
    export_table_to_excel("users", "users_database.xlsx")

    # Експорт таблиці sales
    export_table_to_excel("sales", "sales_database.xlsx")

    # Відправка обох файлів користувачеві
    await message.answer_document(document=open("users_database.xlsx", "rb"), caption="Таблиця з користувачами експортована")
    await message.answer_document(document=open("sales_database.xlsx", "rb"), caption="Таблиця з продажами експортована")

    # Видалення файлів після відправки
    os.remove("users_database.xlsx")
    os.remove("sales_database.xlsx")

