from aiogram import types

async def main_menu(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Продати \U0001F4B0')
    itembtn3 = types.KeyboardButton('Партнерам \U0001F4E2')
    itembtn2 = types.KeyboardButton('Фільтр🔎')
    markup.add(itembtn1, itembtn2, itembtn3)

    # Надсилаємо повідомлення разом з клавіатурою
    await bot.send_message(chat_id, "Виберіть опцію:", reply_markup=markup)
    
    

    
    
def get_categories_keyboard(selected_categories):
    categories_keyboard = types.InlineKeyboardMarkup(row_width=2)
    categories_keyboard.add(
        types.InlineKeyboardButton(text="Телефони" + (" ✅" if "Телефон" in selected_categories else ""), callback_data="Телефон"),
        types.InlineKeyboardButton(text="Навушники" + (" ✅" if "Навушники" in selected_categories else ""), callback_data="Навушники"),
        types.InlineKeyboardButton(text="Ноутбуки" + (" ✅" if "Ноутбук" in selected_categories else ""), callback_data="Ноутбук"),
        types.InlineKeyboardButton(text="Планшети" + (" ✅" if "Планшет" in selected_categories else ""), callback_data="Планшет"),
        types.InlineKeyboardButton(text="Приставки" + (" ✅" if "Приставка" in selected_categories else ""), callback_data="Приставка"),
        types.InlineKeyboardButton(text="Годинники" + (" ✅" if "Годинники" in selected_categories else ""), callback_data="Годинники"),
        types.InlineKeyboardButton(text="Телевізори" + (" ✅" if "Телевізор" in selected_categories else ""), callback_data="Телевізор"),
        types.InlineKeyboardButton(text="Акустика" + (" ✅" if "Акустика" in selected_categories else ""), callback_data="Акустика"),
        types.InlineKeyboardButton(text="Фотоапарати" + (" ✅" if "Фотоапарат" in selected_categories else ""), callback_data="Фотоапарат"),
        types.InlineKeyboardButton(text="Шурупокрути" + (" ✅" if "Шурупокрут" in selected_categories else ""), callback_data="Шурупокрут"),
        types.InlineKeyboardButton(text="Болгарки" + (" ✅" if "Болгарка" in selected_categories else ""), callback_data="Болгарка"),
        types.InlineKeyboardButton(text="Лобзики" + (" ✅" if "Лобзик" in selected_categories else ""), callback_data="Лобзик"),
        types.InlineKeyboardButton(text="Шліфувачі" + (" ✅" if "Шліфувач" in selected_categories else ""), callback_data="Шліфувач"),
        types.InlineKeyboardButton(text="Фени" + (" ✅" if "Фен" in selected_categories else ""), callback_data="Фен"),
        types.InlineKeyboardButton(text="Лазерні" + (" ✅" if "Лазер" in selected_categories else ""), callback_data="Лазер"),
        types.InlineKeyboardButton(text="Зварювач" + (" ✅" if "Зварювач" in selected_categories else ""), callback_data="Зварювач"),
        types.InlineKeyboardButton(text="Генератори" + (" ✅" if "Генератор" in selected_categories else ""), callback_data="Генератор"),
        types.InlineKeyboardButton(text="Бензопили" + (" ✅" if "Бензопила" in selected_categories else ""), callback_data="Бензопила"),
        types.InlineKeyboardButton(text="Електроплити" + (" ✅" if "Електроплита" in selected_categories else ""), callback_data="Електроплита"),
        types.InlineKeyboardButton(text="Кущорізи" + (" ✅" if "Кущоріз" in selected_categories else ""), callback_data="Кущоріз"),
        types.InlineKeyboardButton(text="Ваги" + (" ✅" if "Ваги" in selected_categories else ""), callback_data="Ваги"),
        types.InlineKeyboardButton(text="Дитячі іграшки" + (" ✅" if "іграшки" in selected_categories else ""), callback_data="іграшки"),
        types.InlineKeyboardButton(text="Пилососи" + (" ✅" if "Пилосос" in selected_categories else ""), callback_data="Пилосос"),
        types.InlineKeyboardButton(text="Праски" + (" ✅" if "Праска" in selected_categories else ""), callback_data="Праска"),
        types.InlineKeyboardButton(text="Стайлери" + (" ✅" if "Стайлер" in selected_categories else ""), callback_data="Стайлер"),
        types.InlineKeyboardButton(text="Кавомолки" + (" ✅" if "Кавомолка" in selected_categories else ""), callback_data="Кавомолка"),
        types.InlineKeyboardButton(text="Мультиварки" + (" ✅" if "Мультиварка" in selected_categories else ""), callback_data="Мультиварка"),
        types.InlineKeyboardButton(text="Бутербродниці" + (" ✅" if "Бутербродниця" in selected_categories else ""), callback_data="Бутербродниця"),
        types.InlineKeyboardButton(text="Чайники" + (" ✅" if "Чайник" in selected_categories else ""), callback_data="Чайник"),
        types.InlineKeyboardButton(text="Обігрівачі" + (" ✅" if "Обігрівач" in selected_categories else ""), callback_data="Обігрівач"),
        types.InlineKeyboardButton(text="Шукати🔎", callback_data="search")
    )
    return categories_keyboard


def generate_categories_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Телефон", callback_data="телефон"),
        types.InlineKeyboardButton("Ноутбуки", callback_data="ноутбук"),
        types.InlineKeyboardButton("Навушники", callback_data="навушники")
    )

    markup.row(
        types.InlineKeyboardButton("Планшет", callback_data="планшет"),
        types.InlineKeyboardButton("Приставка", callback_data="приставка"),
        types.InlineKeyboardButton("Годинники", callback_data="годинник")
    )
    markup.row(
        types.InlineKeyboardButton("Телевізор", callback_data="телевізор"),
        types.InlineKeyboardButton("Акустика", callback_data="акустика"),
        types.InlineKeyboardButton("Фотоапарат", callback_data="фотоапарат")
    )
    markup.row(
        types.InlineKeyboardButton("Шурупокрут", callback_data="шурупокрут"),
        types.InlineKeyboardButton("Болгарка", callback_data="болгарка"),
        types.InlineKeyboardButton("Лобзик", callback_data="лобзик")
    )
    markup.row(
        types.InlineKeyboardButton("Шліфувач", callback_data="шліфувач"),
        types.InlineKeyboardButton("Фен", callback_data="фен"),
        types.InlineKeyboardButton("Лазер", callback_data="лазер")
    )
    markup.row(
        types.InlineKeyboardButton("Зварювач", callback_data="зварювач"),
        types.InlineKeyboardButton("Генератор", callback_data="генератор"),
        types.InlineKeyboardButton("Бензопила", callback_data="бензопила")
    )
    markup.row(
        types.InlineKeyboardButton("Електроплита", callback_data="електроплита"),
        types.InlineKeyboardButton("Кущоріз", callback_data="кущоріз"),
        types.InlineKeyboardButton("Ваги", callback_data="ваги")
    )
    markup.row(
        types.InlineKeyboardButton("іграшки", callback_data="іграшка"),
        types.InlineKeyboardButton("Пилосос", callback_data="пилосос"),
        types.InlineKeyboardButton("Праска", callback_data="праска")
    )
    markup.row(
        types.InlineKeyboardButton("Стайлер", callback_data="стайлер"),
        types.InlineKeyboardButton("Кавомолка", callback_data="кавомолка"),
        types.InlineKeyboardButton("Мультиварка", callback_data="мультиварка")
    )
    markup.row(
        types.InlineKeyboardButton("Бутербродниця", callback_data="бутербродниця"),
        types.InlineKeyboardButton("Чайник", callback_data="чайник"),
        types.InlineKeyboardButton("Обігрівач", callback_data="обігрівач")
    )
    markup.row(
        types.InlineKeyboardButton("Інше", callback_data="Інше")
        
    )
    return markup