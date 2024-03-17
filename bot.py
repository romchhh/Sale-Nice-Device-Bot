# -*- coding: utf-8 -*-
import os, glob, aiofiles, asyncio, shutil, io
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, GROUP_ID, ADMIN_IDS, SESSION_NAME, API_HASH, API_ID, channels
from user.user_keyboard import main_menu, get_categories_keyboard, generate_categories_keyboard
from user.user_db import create_table, add_user, add_phone_number_to_user, add_sale
from aiogram.types import InputMediaPhoto, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telethon.sync import TelegramClient
from admin.admin_keyboard import admin_keyboard
from admin.admin_db import get_active_users_count, get_sales_count, get_users_count
from admin.admin_func import export_database_to_excel
from aiogram.utils.exceptions import CantParseEntities




bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

item_info = {}
max_photos = 4
photo_counter = {}
description_sent = {}
next_photo_message_sent = {}


# Обробник для команди /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    greeting_message = f"Вітаємо вас, {first_name}!"
    create_table()
    add_user(chat_id, username, first_name, last_name)
    await check_and_delete_user_folder(message.from_user.id, chat_id)
    await bot.send_message(chat_id, greeting_message)
    await main_menu(bot, chat_id)



"""ADMIN"""
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        await bot.send_message(chat_id, "Ви увійшли до панелі адміністратора.", reply_markup=admin_keyboard)
        
@dp.message_handler(lambda message: message.text == 'Статистика 📊')
async def statistics_handler(message: types.Message):
    total_users = get_users_count()
    active_users = get_active_users_count()
    total_sales = get_sales_count()

    response_message = (
        f"👥 Загальна кількість користувачів: {total_users}\n"
        f"📱 Кількість активних користувачів: {active_users}\n"
        f"🛍️ Загальна кількість продажів: {total_sales}"
    )
    await message.answer(response_message)

@dp.message_handler(lambda message: message.text == 'Вигрузити базу даних 💾')
async def export_database_handler(message: types.Message):
    await message.answer("Вигружаємо базу даних...")
    await export_database_to_excel(message)
    
        
@dp.message_handler(lambda message: message.text == 'Назад в меню ◀️')
async def back_to_menu_handler(message: types.Message):
    await main_menu(bot, message.chat.id)

"""USER"""


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
selected_categories = {}
post_batches = {}

async def get_posts(categories, start_index, batch_size=7, download_batch_size=7, user_id=None):
    async with client:
        found_posts = []

        for channel_name in channels:
            channel_entity = await client.get_entity(channel_name)
            messages = await client.get_messages(channel_entity, limit=400)  # Отримуємо всі повідомлення

            for message in messages:
                message_text_lower = message.message.lower() if message.message else ''
                if any(category.lower() in message_text_lower for category in categories):
                    found_posts.append(message)

        # Вибираємо пости на основі start_index та batch_size
        end_index = start_index + batch_size
        batch = found_posts[start_index:end_index]

        # Створюємо папку користувача
        user_folder = f"user_category_{user_id}"
        os.makedirs(user_folder, exist_ok=True)

        # Завантажуємо фотографії партіями
        for i in range(0, len(batch), download_batch_size):
            batch_subset = batch[i:i + download_batch_size]
            tasks = [download_photo(photo, user_folder) for photo in batch_subset if photo.photo]
            await asyncio.gather(*tasks)

        return batch, end_index

async def download_photo(message, user_folder):
    photo = message.photo
    file_path = await client.download_media(photo, file=os.path.join(user_folder, f'{photo.id}.jpg'))
    print(f'Downloaded photo: {file_path}')
    message.photo_path = file_path  # Зберігаємо шлях до фотографії в об'єкті повідомлення


@dp.callback_query_handler(lambda call: call.data == 'search')
async def search_callback(callback_query: types.CallbackQuery):
    print("Обрані категорії:")
    for category in selected_categories.get(callback_query.message.chat.id, []):
        print(category)
    await bot.send_message(callback_query.message.chat.id, "Проводимо пошук по каналах....")

    # Initialize post batches for the current user
    post_batches[callback_query.message.chat.id] = {"posts": [], "index": 0}

    # Get the first batch of posts
    user_id = callback_query.message.chat.id
    batch, index = await get_posts(selected_categories.get(user_id, []), 0, user_id=user_id)
    post_batches[user_id]["posts"] = batch
    post_batches[user_id]["index"] = index

    if batch:
        for post in batch:
            await send_post_with_button(callback_query.message.chat.id, post)

        if len(batch) >= 7:
            await bot.send_message(callback_query.message.chat.id, "Відправити ще 7 оголошень?", reply_markup=get_pagination_keyboard())
        else:
            await bot.send_message(callback_query.message.chat.id, "Це всі оголошення в даній категорії.")
    else:
        await bot.send_message(callback_query.message.chat.id, "На жаль, нічого не знайдено.")

    # Clean up user-specific directory
    user_folder = f"user_category_{user_id}"
    shutil.rmtree(user_folder, ignore_errors=True)




def get_pagination_keyboard():
    keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Так ✅", callback_data="send_more"))
    keyboard.add(types.InlineKeyboardButton(text="Завершити пошук ❌", callback_data="finish_search"))
    return keyboard


async def send_post_with_button(chat_id, post):
    has_error = False

    if post.photo_path:
        with open(post.photo_path, 'rb') as photo:
            try:
                await bot.send_photo(chat_id, photo, caption=post.text, parse_mode="Markdown")
            except CantParseEntities:
                print(f"Can't parse entities in post: {post.text}")
                has_error = True
    else:
        try:
            await bot.send_message(chat_id, post.text, parse_mode="Markdown")
        except CantParseEntities:
            print(f"Can't parse entities in post: {post.text}")
            has_error = True

    if not has_error:
        await bot.send_message(chat_id, "🤩Зацікавив пост?🤩", reply_markup=get_post_button(post))


def get_post_button(post):
    inline_keyboard = types.InlineKeyboardMarkup()
    post_link = f"https://t.me/{post.chat.username}/{post.id}"
    inline_keyboard.add(types.InlineKeyboardButton(text="Перейти до поста", url=post_link))
    return inline_keyboard

@dp.callback_query_handler(lambda call: call.data == 'send_more')
async def send_more_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    batch_size = 7

    if chat_id in post_batches:
        start_index = post_batches[chat_id]["index"]
        batch, index = await get_posts(selected_categories.get(chat_id, []), start_index, user_id=chat_id)

        if batch:
            post_batches[chat_id]["posts"].extend(batch)
            post_batches[chat_id]["index"] = index

            for post in batch:
                await send_post_with_button(chat_id, post)

            if len(batch) >= 7:
                await bot.send_message(chat_id, "Відправити ще 10?", reply_markup=get_pagination_keyboard())
            else:
                await bot.send_message(chat_id, "Це всі оголошення в даній категорії.")
        else:
            del post_batches[chat_id]
            await bot.send_message(chat_id, "Більше постів немає.")

        user_folder = f"user_category_{chat_id}"
        shutil.rmtree(user_folder, ignore_errors=True)
    else:
        await bot.send_message(chat_id, "Пошук було завершено.")


@dp.callback_query_handler(lambda call: call.data == 'finish_search')
async def finish_search_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    if chat_id in post_batches:
        del post_batches[chat_id]  
        await bot.send_message(chat_id, "Пошук завершено.")
        
    else:
        await bot.send_message(chat_id, "Пошук було завершено.")
        
    user_folder = f"user_category_{chat_id}"
    shutil.rmtree(user_folder, ignore_errors=True)





@dp.message_handler(lambda message: message.text == 'Фільтр🔎')
async def filter(message: types.Message):
    if message.chat.id not in selected_categories:
        selected_categories[message.chat.id] = []
    categories_keyboard = get_categories_keyboard(selected_categories[message.chat.id])
    await bot.send_message(message.chat.id, "Виберіть категорії:", reply_markup=categories_keyboard)
    
    user_id = message.chat.id  # Obtain user_id from the message object
    category_folder = f"user_category_{user_id}"
    if os.path.exists(category_folder):
        shutil.rmtree(category_folder)
    

@dp.callback_query_handler(lambda call: call.data in ['Телефон', 'Навушники', 'Ноутбук', 'Планшет', 'Приставка','Годинники', 'Телевізор', 'Акустика', 'Фотоапарат', 'Шурупокрут', 'Болгарка', 'Лобзик', 'Ноутбук', 'Шліфувач', 'Фен','Лазер', 'Зварювач', 'Генератор', 'Бензопила', 'Електроплита','Кущоріз', 'Ваги', 'іграшки', 'Пилосос', 'Праска','Стайлер', 'Кавомолка', 'Мультиварка', 'Бутербродниця', 'Чайник', 'Обігрівач'])
async def process_callback(callback_query: types.CallbackQuery):
    buy_category = callback_query.data
    if callback_query.message.chat.id not in selected_categories:
        selected_categories[callback_query.message.chat.id] = []
    if buy_category in selected_categories[callback_query.message.chat.id]:
        selected_categories[callback_query.message.chat.id].remove(buy_category)
    else:
        selected_categories[callback_query.message.chat.id].append(buy_category)
    categories_keyboard = get_categories_keyboard(selected_categories[callback_query.message.chat.id])
    if categories_keyboard != callback_query.message.reply_markup:
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=categories_keyboard)


@dp.message_handler(lambda message: message.text == 'Партнерам \U0001F4E2')
async def partners(message: types.Message):
    await bot.send_message(message.chat.id, "З приводу партнерства звертайтесь до @Andriy1.")
    
    user_id = message.chat.id  # Obtain user_id from the message object
    category_folder = f"user_category_{user_id}"
    if os.path.exists(category_folder):
        shutil.rmtree(category_folder)
    

@dp.message_handler(lambda message: message.text == 'Продати \U0001F4B0')
async def sell(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Надіслати номер телефону📞', request_contact=True))
    markup.add(types.KeyboardButton('🔙Назад'))

    await bot.send_message(message.chat.id, "Натисніть кнопку, щоб надіслати свій номер телефону:", reply_markup=markup)
    
    user_id = message.chat.id  # Obtain user_id from the message object
    category_folder = f"user_category_{user_id}"
    if os.path.exists(category_folder):
        shutil.rmtree(category_folder)

@dp.message_handler(content_types=['contact'])
async def contact_received(message: types.Message):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    add_phone_number_to_user(user_id, phone_number)

    back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_markup.add(types.KeyboardButton('🔙Назад'))

    markup = generate_categories_keyboard()

    item_info[str(user_id)] = {
        'phone_number': phone_number,
        'category': None,
        'description': None,
        'photos': []
    }
    photo_counter[str(user_id)] = 0  
    description_sent[str(user_id)] = False 
    next_photo_message_sent[str(user_id)] = False 

    await bot.send_message(message.chat.id, "Ваш номер телефону успішно збережено.", reply_markup=back_markup)
    await bot.send_message(message.chat.id, "Оберіть категорію:", reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data in ['телефон', 'навушники', 'ноутбук', 'планшет', 'приставка','годинник', 'телевізор', 'акустика', 'фотоапарат', 'шурупокрут', 'болгарка', 'лобзик', 'ноутбук', 'шліфувач', 'фен','лазер', 'зварювач', 'генератор', 'бензопила', 'електроплита','кущоріз', 'ваги', 'іграшка', 'пилосос', 'праска', 'стайлер', ' кавомолка', 'мультиварка', 'бутербродниця', 'чайник', 'обігрівач', 'Інше'])
async def category_chosen(call: types.CallbackQuery):
    sell_category = call.data
    user_id = call.message.chat.id
    item_info[str(user_id)]['category'] = sell_category

    await bot.answer_callback_query(callback_query_id=call.id, text='Оберіть фото товару')
    chosen_category_text = f"Ви обрали категорію {sell_category}\nНадішліть фото товару:"
    await bot.send_message(user_id, chosen_category_text)
    
@dp.message_handler(content_types=['photo'])
async def photo_received(message: types.Message):
    user_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    downloaded_bytes = downloaded_file.getvalue()

    user_dir = f'user_{user_id}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    file_extension = os.path.splitext(file_info.file_path)[1]
    file_name = f'{user_id}_{file_id}{file_extension}'
    file_path = os.path.join(user_dir, file_name)
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(downloaded_bytes)

    item_info[str(user_id)]['photos'].append(file_path)
    photo_counter[str(user_id)] += 1  

    if photo_counter[str(user_id)] <= max_photos and not description_sent[str(user_id)]:
        await bot.send_message(user_id, 'Фото успішно отримано. Надішліть опис товару.')
        description_sent[str(user_id)] = True 

    elif photo_counter[str(user_id)] <= max_photos and description_sent[str(user_id)] and not next_photo_message_sent[str(user_id)]:
        next_photo_message_sent[str(user_id)] = True

stored_messages = {}

@dp.message_handler(lambda message: message.text != '🔙Назад')
async def description_received(message: types.Message):
    user_id = message.chat.id
    description = message.text

    if str(user_id) not in item_info:
        item_info[str(user_id)] = {
            'phone_number': None,
            'category': None,
            'description': None,
            'photos': []
        }

    item_info[str(user_id)]['description'] = description

    if str(user_id) not in description_sent:
        description_sent[str(user_id)] = False

    if description_sent[str(user_id)]:
        if str(user_id) not in item_info:
            return

        user = await bot.get_chat(user_id)
        phone_number = item_info[str(user_id)]['phone_number']
        category = item_info[str(user_id)]['category']
        preview_message = f"<b>Опис товару:</b> {description} \n<b>Категорія:</b> {category}\n<b>Номер телефону:</b> {phone_number}\n<b>Користувач: @</b>{user.username}"

        photo_data = []
        for photo_path in item_info[str(user_id)]['photos']:
            with open(photo_path, 'rb') as f:
                photo_data.append((f.read(), os.path.basename(photo_path)))

        if len(photo_data) == 1:
            file_obj = io.BytesIO(photo_data[0][0])
            input_file = InputFile(file_obj, filename=photo_data[0][1])
            media_group_result = await bot.send_photo(user_id, input_file, caption=preview_message, parse_mode='HTML')
        else:
            input_media_photos = []
            for i, (photo_bytes, file_name) in enumerate(photo_data):
                file_obj = io.BytesIO(photo_bytes)
                input_file = InputFile(file_obj, filename=file_name)
                if i == len(photo_data) - 1:
                    input_media_photos.append(InputMediaPhoto(media=input_file, caption=preview_message, parse_mode='HTML'))
                else:
                    input_media_photos.append(InputMediaPhoto(media=input_file))

            media_group_result = await bot.send_media_group(user_id, input_media_photos)

        keyboard = InlineKeyboardMarkup(row_width=2)
        send_button = InlineKeyboardButton("Надіслати", callback_data="send_post")
        cancel_button = InlineKeyboardButton("Скасувати", callback_data="cancel_post")
        keyboard.add(send_button, cancel_button)

        message_sent = await bot.send_message(
            message.chat.id,
            "Все вірно?",
            reply_markup=keyboard
        )  

        if str(user_id) in photo_counter:
            photo_counter[str(user_id)] = 0
        if str(user_id) in description_sent:
            description_sent[str(user_id)] = False
        if str(user_id) in next_photo_message_sent:
            next_photo_message_sent[str(user_id)] = False

        return message_sent.message_id

@dp.callback_query_handler(lambda query: query.data == 'send_post')
async def send_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if str(user_id) not in item_info:
        return

    user_folder = f'user_{user_id}'
    photo_paths = glob.glob(f'{user_folder}/*.jpg') + glob.glob(f'{user_folder}/*.jpeg') + glob.glob(f'{user_folder}/*.png')
    photo_data = []
    for photo_path in photo_paths:
        with open(photo_path, 'rb') as f:
            photo_data.append((f.read(), os.path.basename(photo_path)))

    if not photo_data:
        await bot.send_message(callback_query.from_user.id, "У вас немає фото для надсилання.")
        return

    user = await bot.get_chat(user_id)
    phone_number = item_info[str(user_id)]['phone_number']
    category = item_info[str(user_id)]['category']
    description = item_info[str(user_id)]['description']
    preview_message = f"<b>Опис товару:</b> {description} \n<b>Категорія:</b> {category}\n<b>Номер телефону:</b> {phone_number}\n<b>Користувач: @</b>{user.username}\n\n\n<em>Шукаєте зручний спосіб продати непотрібний девайс?</em> Перейдіть за <a href='https://t.me/SaleNiceDeviceBot'><u>посиланням</u></a> і дізнайтеся, як просто та швидко знайти покупця для вашого пристрою."


    channel_message = "🔝 🔝 🔝"
    

    input_media_photos = []
    if len(photo_data) == 1:
        file_obj = io.BytesIO(photo_data[0][0])
        input_file = InputFile(file_obj, filename=photo_data[0][1])
        
        await bot.send_message(GROUP_ID, channel_message, parse_mode='HTML')
        media_group_result = await bot.send_photo(GROUP_ID, input_file, caption=preview_message, parse_mode='HTML')
    else:
        input_media_photos = []
        for i, (photo_bytes, file_name) in enumerate(photo_data):
            file_obj = io.BytesIO(photo_bytes)
            input_file = InputFile(file_obj, filename=file_name)
            if i == len(photo_data) - 1:
                input_media_photos.append(InputMediaPhoto(media=input_file, caption=preview_message, parse_mode='HTML'))
            else:
                input_media_photos.append(InputMediaPhoto(media=input_file))
                
        await bot.send_message(GROUP_ID, channel_message, parse_mode='HTML')
        media_group_result = await bot.send_media_group(GROUP_ID, input_media_photos)

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.add(InlineKeyboardButton("Написати продавцю", url=f"https://t.me/{user.username}"))
    await bot.send_message(GROUP_ID, "🤩Зацікавило оголошення?🤩", reply_markup=keyboard_markup)
    
    await bot.send_message(user_id, "Ваш пост успішно надіслано!")
    await main_menu(bot, callback_query.message.chat.id)

    add_sale(
        user_id=user_id,
        phone_number=item_info[str(user_id)]['phone_number'],
        category=item_info[str(user_id)]['category'],
        description=description,
        photos=item_info[str(user_id)]['photos']
    )

    shutil.rmtree(user_folder)

    item_info[str(user_id)] = {
        'phone_number': item_info[str(user_id)]['phone_number'],
        'category': None,
        'description': None,
        'photos': []
    }

    item_info.pop(str(user_id), None)

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)

    
@dp.callback_query_handler(lambda query: query.data == 'cancel_post')
async def cancel_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if str(user_id) not in item_info:
        return

    user_folder = f'user_{user_id}'
    shutil.rmtree(user_folder)
    item_info.pop(str(user_id), None)
    
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, "Скасовано")
    await main_menu(bot, callback_query.message.chat.id)
    
    
async def check_and_delete_user_folder(user_id, chat_id):
    user_folder = f"user_{user_id}"
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)

    # Перевірка і видалення папки user_category_{user_id}
    category_folder = f"user_category_{user_id}"
    if os.path.exists(category_folder):
        shutil.rmtree(category_folder)

        


@dp.message_handler(lambda message: message.text == '🔙Назад')
async def back_to_main_menu(message: types.Message):
    user_folder = f"user_{message.from_user.id}"
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        await main_menu(bot, message.chat.id)
    else:
        await main_menu(bot, message.chat.id)

if __name__ == '__main__':
    try:
        client.start()
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
    finally:
        client.disconnect()
