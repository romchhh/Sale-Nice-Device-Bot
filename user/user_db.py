import sqlite3

def create_table():
    """Створює таблицю для збереження інформації про користувачів."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_user(chat_id, username, first_name, last_name):
    """Додає дані про користувача до бази даних, якщо його ще немає в базі."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    # Перевіряємо, чи існує користувач з таким chat_id в базі даних
    cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    existing_user = cursor.fetchone()
    if existing_user is None:
        # Якщо користувача з таким chat_id ще немає в базі, додаємо його
        cursor.execute('''
            INSERT INTO users (chat_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, username, first_name, last_name))
        conn.commit()
    conn.close()
    
def add_phone_number_to_user(chat_id, phone_number):
    """Додає номер телефону користувача до запису у базі даних."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET phone = ?
        WHERE chat_id = ?
    ''', (phone_number, chat_id))
    conn.commit()
    conn.close()
    
def find_photo_matches(photo_hash: bytes) -> list:
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()

    # Знайти всі фотографії з гешем, який збігається з заданим
    cursor.execute("SELECT * FROM photos WHERE hash=?", (photo_hash,))
    matches = cursor.fetchall()

    conn.close()

    return matches


def add_photos_info(photos_info: list):
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()

    # Додати інформацію про фотографії до бази даних
    cursor.executemany("""
        INSERT INTO photos (channel_id, channel_name, msg_id, date, link, hash)
        VALUES (?, ?, ?, ?, ?, ?)
    """, photos_info)

    conn.commit()
    conn.close()

    
    
import json

def add_sale(user_id, phone_number, category, description, photos):
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    photos_json = json.dumps(photos)  # Serialize photos to JSON string
    cursor.execute("INSERT INTO sales (user_id, phone, category, description, photos) VALUES (?, ?, ?, ?, ?)",
                   (user_id, phone_number, category, description, photos_json))
    conn.commit()
    conn.close()
