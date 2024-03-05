from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📝 Профиль", callback_data="profile"),
    InlineKeyboardButton(text="🔗 Ресурсы", callback_data="resources")],
    [InlineKeyboardButton(text="🔼 Уровень", callback_data="level"),
    InlineKeyboardButton(text="💳 Баланс", callback_data="balance")],
    [InlineKeyboardButton(text="💎Партнёр", callback_data="partners"),
    InlineKeyboardButton(text="🎁 Бонусы", callback_data="bonuses")],
    [InlineKeyboardButton(text="🔎 Инфо", callback_data="info")]
]
bonus_button = [[InlineKeyboardButton(text="🎁 Открыть Бонус", callback_data="get_bonus")]]
share_button = [[InlineKeyboardButton(text="🔗 Поделиться", callback_data="share")]]
transfer_button = [[InlineKeyboardButton(text=" Перевод", callback_data="transfer")]]
pay_button = [[InlineKeyboardButton(text=" Оплата", callback_data="pay")]]


menu_markup = InlineKeyboardMarkup(inline_keyboard=menu)
bonus_button = InlineKeyboardMarkup(inline_keyboard=bonus_button)
share_button = InlineKeyboardMarkup(inline_keyboard=share_button)
transfer_button = InlineKeyboardMarkup(inline_keyboard=transfer_button)
pay_button = InlineKeyboardMarkup(inline_keyboard=pay_button)

"1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣0️⃣"

button1 = KeyboardButton(text="📍Меню")
button2 = KeyboardButton(text="🪪Профиль")
button3 = KeyboardButton(text="🔼Уровень")
button4 = KeyboardButton(text="💳Баланс")
button5 = KeyboardButton(text="💎Партнеры")
button6 = KeyboardButton(text="🔗Ресурсы")
button7 = KeyboardButton(text="🎁Бонусы")
button8 = KeyboardButton(text="🔎Инфо")

reply_markup = ReplyKeyboardMarkup(keyboard=[[button1, button2, button3, button4], [button5, button6, button7, button8]], resize_keyboard=True)





# builder = InlineKeyboardBuilder()
# for i in range(15):
#     builder.button(text=f”Кнопка {i}”, callback_data=f”button_{i}”)
# builder.adjust(2)
# await msg.answer(“Текст сообщения”, reply_markup=builder.as_markup())

