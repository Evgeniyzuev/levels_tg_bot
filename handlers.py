import kb
import texts
import utils
import config
import database #import SessionLocal, User
from datetime import datetime, timedelta
import re

from aiogram import types, F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from sqlalchemy.sql import func
from aiogram.methods.get_chat import GetChat


from misc import dp, bot
from states import Gen

# START
# @dp.message(Command("start"))
@dp.message(CommandStart(deep_link=True))
async def start_handler( callback_query: types.CallbackQuery, command: CommandObject): #message: Message,
    # user_id = callback_query.message.from_user.id

    try:
        user_name = callback_query.from_user.full_name
        user_id = callback_query.from_user.id
        await bot.send_message(user_id, f"{user_name}, привет! Рад видеть! 🤗")
    finally:
        pass

# Referrer ID
    try:
        args = command.args
        referrer_id = decode_payload(args)
    except:
        await bot.send_message(user_id, text='❗️ Не могу расшифровать реферальную ссылку ❗️')
        referrer_id = 0

    await bot.send_message(user_id, text=f'ВНИМАНИЕ❗️❗️❗️\nБот работает в тестовом режиме\n❗️Никаких выплат не будет до релиза')


 # TRRRRRYYYY DATABASE
    # TRRRRRYYYY DATABASE

    referral_link = await create_start_link(bot,str(user_id), encode=True)
    user = await database.get_or_create_user(user_id, user_name, referral_link, referrer_id)
    if user.bonuses_gotten < 2 :
        try:
            await bot.send_message(referrer_id, text= f"По вашей ссылке зашел пользователь:\n{user_name}\nВы получите бонус 🎁 когда пользователь откроет два бонуса.")
        finally:
            pass 




    # Просто пестня. Оно работает!
    # user_info_text = await database.user_info(user_id)
    # await callback_query.answer(user_info_text)
    await utils.start_guide_stages(user_id)


@dp.message(Command("start"))
async def start_handler( callback_query: types.CallbackQuery): #message: Message,
    user_id = callback_query.from_user.id
    # chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.full_name
    try:
        await bot.send_message(user_id, f"{user_name}, привет!\nВсегда рад видеть! 🤗")
    finally:
        pass
    await utils.start_guide_stages(user_id)



# Нажатие кнопки открыть бонус
@dp.callback_query(F.data == "open_bonus")
async def process_open_bonus_button(callback_query: types.CallbackQuery): #message: Message, 
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    # chat_id =  await bot.get_chat()
    user = await database.get_user(user_id)
    bonuses_gotten = user.bonuses_gotten
    bonuses_available = user.bonuses_available
    if bonuses_available > 0:
        if bonuses_gotten-bonuses_available == 1:
            try:
                current_leader_id = user.current_leader_id
                await bot.send_message(current_leader_id, text= f"Ваш реферал: {user_name}(ID: {user_id}) открыл второй бонус.", reply_markup=kb.get_and_open_bonus_button)
            except:
                await bot.send_message(user_id, text="не получилось")   
    await utils.open_bonus(user_id)
    if user.guide_stage == 1:
        await utils.start_guide2(user_id)  
    elif user.guide_stage == 3:
        await utils.start_guide4(user_id)


# # Запрос проверить оплату
# @dp.callback_query(F.data == "check_user_payment")
# async def process_check_payment(callback_query: types.CallbackQuery): #message: Message,    
#     user_id = callback_query.from_user.id
#     # user_name = callback_query.from_user.full_name
#     # chat_id =  await bot.get_chat()
#     user = await database.get_user(user_id)
#     # bonuses_gotten = user.bonuses_gotten
#     # bonuses_available = user.bonuses_available
#     # if bonuses_available > 0:
#     #     if bonuses_gotten-bonuses_available == 1:
#     #         try:
#     #             current_leader_id = user.current_leader_id
#     await bot.send_message(config.levels_guide_id, text= f":Запрос подтверждение на сумму:{database.gamma}; (ID:{user_id};)", reply_markup=kb.admin_confirm_payment)

#     # await bot.send_message(user_id, text="не получилось")   





    # user = database.get_user(user_id)
    # user.grow_wallet+=database.payment_to_check[user_id]
    

    # database.gamma[user_id] = 0
    # database.payment_to_check[user_id] = 0
    # await bot.edit_message_reply_markup(user_id, message_id=callback_query.message.message_id, reply_markup=None )
    # await bot.send_message(user_id, text="Оплата подтверждена")






# Нажатие кнопки получать бонус за реферала
@dp.callback_query(F.data == "get_and_open_bonus")
async def process_get_and_open_bonus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.edit_message_reply_markup(user_id, message_id=callback_query.message.message_id, reply_markup=None )
    await utils.add_bonus(user_id)
    await bot.send_message(user_id, text="+🎁 Бонус получен!\nОткройте его на вкладке Бонусы")

@dp.callback_query(F.data == "up_level")
async def process_up_level(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    current_leader = await database.get_user(user.current_leader_id)
    if user.level < current_leader.level:
        await utils.up_level(user_id)
    else:
        await bot.send_message(user_id, text="У вашего Лида нет next level.\n\nВы можете выбрать Лида\nВкладка партнеры\nНаставники доступны:")
    # await bot.send_message(user_id, 'Лид не найден')

@dp.callback_query(F.data == "up_me") 
async def process_up_me(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await utils.up_me(user_id)

# TODO: Ввод суммы вручную
@dp.callback_query(F.data == "add_grow") 
async def process_add_grow(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, f'Пополнение grow_wallet:\n\n + {database.gamma[user_id]} рублей'+ texts.add_grow_text, reply_markup=kb.add_balance_ready)

@dp.callback_query(F.data == "add_balance_ready") 
async def process_add_balance_ready(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await utils.add_balance_ready(user_id)

# TODO: Проверка платежа. Надо спарсить user_id из сообщения и ввести сумму вручную и подтвердить
@dp.callback_query(F.data == "admin_confirm_payment")
async def process_confirm_payment_button(callback_query: types.CallbackQuery): #message: Message, callback_query: types.CallbackQuery, 
    text = callback_query.message.text
    # id_string = re.search(r'(?<=ID:)(.*)(?=;)', str(text))
    # amount_string = re.search(r'(?<=:)(.*)(?=;)', str(text))
    # user_id = int(str(id_string))
    # amount = int(amount_string.group())
    splitted = str(text).split(';')
    user_id = splitted[1]
    amount = splitted[0]
    user_id = int(user_id)
    amount = int(amount)
    user = await database.get_user(user_id)
   
    await utils.add_grow(user_id, amount)
    await utils.add_turnover(user_id, amount)
    await bot.edit_message_reply_markup(config.levels_guide_id, message_id=callback_query.message.message_id, reply_markup=None )
    await bot.send_message(user_id, f'Пополнение grow_wallet:\n + {amount} рублей' )



    # TODO: Проверка платежа. Надо спарсить user_id из сообщения и ввести сумму вручную и подтвердить
@dp.callback_query(F.data == "admin_change_amount_payment")
async def process_confirm_payment_button(callback_query: types.CallbackQuery): #message: Message, callback_query: types.CallbackQuery, 
    text = callback_query.message.text
    # id_string = re.search(r'(?<=ID:)(.*)(?=;)', str(text))
    # amount_string = re.search(r'(?<=:)(.*)(?=;)', str(text))
    # user_id = int(str(id_string))
    # amount = int(amount_string.group())
    splitted = str(text).split(';')
    user_id = splitted[1]
    amount = splitted[0]
    user_id = int(user_id)
    amount = int(amount)
    # user = await database.get_user(user_id)

    # user_id = str(callback_query.message.text).split(';')
    # amount = str(callback_query.message.text).split(';')
  
    database.payment_to_check_user_id = user_id
    # database.gamma[user_id] = 0
    # database.payment_to_check[user_id] = 0
    await bot.edit_message_reply_markup(config.levels_guide_id, message_id=callback_query.message.message_id, reply_markup=None )
    await bot.send_message(config.levels_guide_id, "введите сумму", reply_markup=kb.changed_amount_payment_confirm )





@dp.callback_query(F.data == "check_subscribe_button")
async def check_subs(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        await utils.start_guide3(user_id)    
    
@dp.callback_query(F.data == "no_subscribtion")
async def check_subs(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    if user.guide_stage == 2:
        await utils.start_guide3_nosub(user_id) 

@dp.callback_query(F.data == "check_done_button")
async def check_done(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    if user.guide_stage == 3:
        await utils.start_guide3_1(user_id)


# SWITCH TABS
swith_tabs_data =      ["menu"   , "profile"   , "resources"   , "level"      , "balance"    , "partners"    , "bonuses"   , "info"     ] 
switch_tabs_text=      ["Меню"   , "Профиль"   , "Ресурсы"     , "Уровень"    , "Баланс"     , "Партнеры"    , "Бонусы"    , "Инфо"     ]
switch_tabs_emoji_text=["📍\nМеню", "🪪\nПрофиль", "🔗\nРесурсы", "🔼\nУровень", "💳\nБаланс", "💎\nПартнеры", "🎁\nБонусы", "🔎\nИнфо"]
switch_tabs_commands = ["/menu"  , "/profile"  , "/resources"    , "/level"     , "/balance"   , "/partners"   , "/bonuses"    , "/info"    ]

@dp.callback_query(F.data)
async def swith_menu_tubs(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data in swith_tabs_data:
        await utils.switch_tubs(data, user_id=callback_query.from_user.id)
        # await bot.answer_callback_query(callback_query.from_user.id)

       
@dp.message(F.text)  
async def swith_menu_tubs(msg: Message):
    if msg.text in switch_tabs_emoji_text:
        index = switch_tabs_emoji_text.index(msg.text)
        data = swith_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    elif msg.text in switch_tabs_text:
        index = switch_tabs_text.index(msg.text)
        data = swith_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    elif msg.text in switch_tabs_commands:
        index = switch_tabs_commands.index(msg.text)
        data = swith_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    # await bot.answer_callback_query(callback_query.id)
        


