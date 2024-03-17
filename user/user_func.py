import os
import shutil
from aiogram import types
from bot import bot, dp, main_menu

@dp.message_handler(lambda message: message.text == '🔙Назад')
async def back_to_main_menu(message: types.Message):
    user_folder = f"user_{message.from_user.id}"
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        await main_menu(bot, message.chat.id)
    else:
        await main_menu(bot, message.chat.id)
        

async def check_and_delete_user_folder(user_id, chat_id):
    user_folder = f"user_{user_id}"
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)

    # Перевірка і видалення папки user_category_{user_id}
    category_folder = f"user_category_{user_id}"
    if os.path.exists(category_folder):
        shutil.rmtree(category_folder)

        

async def back_to_main_menu(message: types.Message):
    await main_menu(bot, message.chat.id)
