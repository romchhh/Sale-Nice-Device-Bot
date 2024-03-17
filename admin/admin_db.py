import sqlite3

def get_users_count():
    """Повертає кількість користувачів у базі даних."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_active_users_count():
    """Повертає кількість активних користувачів у базі даних."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE phone IS NOT NULL")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_sales_count():
    """Повертає кількість продажів у базі даних."""
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_user_ids():
    conn = sqlite3.connect('db/data.db')  # Подставьте свой путь к файлу базы данных SQLite
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return user_ids


