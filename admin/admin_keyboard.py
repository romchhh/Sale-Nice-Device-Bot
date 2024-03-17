from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
admin_keyboard.add(KeyboardButton('Статистика 📊'), KeyboardButton('Вигрузити базу даних 💾'))
admin_keyboard.add(KeyboardButton('Назад в меню ◀️'))
