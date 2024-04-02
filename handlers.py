import kb
import texts
import utils
import config
import database #import SessionLocal, User

from misc import dp, bot


from aiogram import types, F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject, StateFilter
from aiogram.utils.deep_linking import create_start_link, decode_payload
from sqlalchemy.sql import func
from aiogram.methods.get_chat import GetChat
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

#     Справочник https://t.me/aiogram/28
#     await callback_query.answer("Как много?",reply_markup=ReplyKeyboardRemove(),)  Всплывающее сообщение и удаление клавиатуры


# класс состояний
class Form(StatesGroup):
    amount_state = State()
    amount_state_ok = State()
    wait_check = State()
    grow_to_liquid = State()
    liquid_wallet_down = State()
    grow_wallet_up = State()
    liquid_to_grow = State()
    restate_up = State()
    restate_down = State()
    admin_send_ckeck_state = State()
    user_send_ckeck_state = State()
    requisites_entering_state = State()



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

    await utils.start_guide_stages(user_id)


@dp.message(Command("start"))
async def start_handler( callback_query: types.CallbackQuery): #message: Message,
    user_id = callback_query.from_user.id
-
    user_name = callback_query.from_user.full_name
    await bot.send_message(user_id, f"{user_name}, привет!\nВсегда рад видеть! 🤗")
    await utils.start_guide_stages(user_id)

@dp.message(Command("morning"))
async def start_handler( callback_query: types.CallbackQuery): #message: Message,
    user_id = callback_query.from_user.id
    if user_id == config.levels_guide_id:
    # user_name = callback_query.from_user.full_name
        await bot.send_message(user_id, f'Инициирую протокол доброе утро')
        await utils.good_morning_all()


# # добавление пользователя в канал
dp.chat_join_request.register(utils.approve_chat_join_request)
 

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


# Выдаёт реквизиты №1 для пополнения grow_wallet
@dp.callback_query(F.data == "add_grow") 
async def process_add_grow(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, f'Пополнение grow_wallet:\n\n + {database.gamma[user_id]} рублей'+ texts.add_grow_text_1, reply_markup=kb.add_balance_ready)

# Передаёт запрос на пополнение админу
@dp.callback_query(F.data == "add_balance_ready")
async def process_add_balance_ready(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    database.payment_to_check_user_id = user_id
    await bot.edit_message_reply_markup(user_id, message_id=callback_query.message.message_id, reply_markup=None )
    # await utils.add_balance_ready(user_id)
    # database.payment_to_check=database.gamma[user_id]
    await bot.send_message(config.levels_guide_id, text= f":Запрашивают подтверждение пополнения баланса. USER (amount;ID)  Пришла?")
    await bot.send_message(config.levels_guide_id, text= f"{database.gamma[user_id]};{user_id}", reply_markup=kb.admin_confirm_payment)
    await state.set_state(Form.user_send_ckeck_state)
    await bot.send_message(user_id, f'Платеж: {database.gamma[user_id]} рублей - ожидает подтверждения\n\nОтправьте боту чек 📎↘️')


@dp.message(StateFilter(Form.user_send_ckeck_state))
async def process_user_send_ckeck_state(message: Message, state: FSMContext) -> None:
    await message.send_copy(config.levels_guide_id)
    await state.set_state(None)
    await bot.send_message(message.from_user.id, f'Платеж в процессе')


# # Изменить сумму платежа вручную
@dp.callback_query(F.data == "admin_change_amount_payment")
async def process_confirm_payment_button(callback_query: types.CallbackQuery, state: FSMContext) -> None: #message: Message, callback_query: types.CallbackQuery, 
    text = callback_query.message.text
    splitted = str(text).split(';')
    user_id = splitted[1]
    user_id = int(user_id)
    database.payment_to_check_user_id = user_id
    await state.set_state(Form.amount_state)
    # await bot.edit_message_reply_markup(config.levels_guide_id, message_id=callback_query.message.message_id, reply_markup=None )
    # await bot.send_message(config.levels_guide_id, "введите сумму", reply_markup=kb.changed_amount_payment_confirm )
    await callback_query.answer("Как много?",reply_markup=ReplyKeyboardRemove(),)

# пополняет по кнопке  ("Деньги вижу")
@dp.callback_query(F.data == "admin_confirm_payment")
async def process_confirm_payment_button(callback_query: types.CallbackQuery): #message: Message, callback_query: types.CallbackQuery, 
    text = callback_query.message.text

    splitted = str(text).split(';')
    user_id = splitted[1]
    amount = splitted[0]
    user_id = int(user_id)
    amount = int(amount)

    await utils.add_grow(user_id, amount)
    await bot.edit_message_reply_markup(config.levels_guide_id, message_id=callback_query.message.message_id, reply_markup=None )
    await bot.send_message(user_id, f'Пополнение grow_wallet:\n + {amount} рублей' )

# Подтвердить введенную сумму?
@dp.message(StateFilter(Form.amount_state))
async def process_amount(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.amount_state_ok)
    await state.update_data(amount=message.text)
    database.payment_to_check_amount = int(message.text)
    await message.answer(f'Пополнение grow_wallet:\n + {message.text} рублей\n\nUser ID: {database.payment_to_check_user_id}',reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Yes"),KeyboardButton(text="No"),]],resize_keyboard=True,),)


# Подтвердить введенную сумму - да
@dp.message(Form.amount_state_ok, F.text.casefold() == "yes")
async def process_amount_state_ok(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    user_id = database.payment_to_check_user_id
    amount = database.payment_to_check_amount
    await utils.add_grow(user_id, amount)
    await bot.send_message(user_id, f'Пополнение grow_wallet:\n + {amount} рублей' )
    await message.answer("Готово",reply_markup=ReplyKeyboardRemove())


# Отменить введенную сумму (нет)
@dp.message(Form.amount_state_ok, F.text.casefold() == "no")
async def process_amount_state_ok(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.amount_state)
    await callback_query.answer("Как много?",) # reply_markup=ReplyKeyboardRemove(),



#движения по счетам  --------------------------------> кнопки
@dp.callback_query(F.data == "grow_to_liquid")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.grow_to_liquid)
    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'\nGrow -> Liquid\nКомиссия за срочность 1%\nДоступно Grow: {user.grow_wallet} \nВведите сумму:')

@dp.message(StateFilter(Form.grow_to_liquid))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        if amount < 0: amount = -1*amount
        if user.grow_wallet < int(amount):
            await message.answer(f'Недостаточно средств')
        else:
            await utils.add_grow(user_id, (-1)*int(amount))
            await utils.add_liquid(user_id, (0.99)*int(amount))
            await message.answer(f'\nGrow -> Liquid:\n{amount} рублей')
    except:
        await message.answer('Введите целое число')
    await state.set_state(None)


@dp.callback_query(F.data == "liquid_wallet_down")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.liquid_wallet_down)
    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'Доступно Liquid: {user.liquid_wallet} рублей\nВведите сумму:')

@dp.message(StateFilter(Form.liquid_wallet_down))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        if amount < 0: amount = -1*amount
        if user.liquid_wallet < amount or user.liquid_wallet <= 0:
            await message.answer(f'Недостаточно средств')
            await state.set_state(None)
        else:
            database.payout[user_id] = amount
            await state.set_state(Form.requisites_entering_state)
            await bot.send_message(user_id, f'\nВывод на TON кошелек +лучший курс\nУкажите номер телефона и адрес кошелька в сети ❗️TON❗️\
                           \n❗️Внимание❗️\nИспользование адреса в другой сети приведет к потере средств❗️\n\nПеревод по СБП без комиссии\nУкажите номер телефона и банк')
    except:
        await message.answer('Введите целое число')
        await state.set_state(None)
    

@dp.message(StateFilter(Form.requisites_entering_state))
async def process_requisites_entering_state(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    await state.update_data(requisites=message.text)
    try:
        requisites = (message.text)
        await bot.send_message(config.levels_guide_id, text= f"Реквизиты: {requisites}")
        await bot.send_message(config.levels_guide_id, text= f"Отправить перевод USER (amount;ID)")
        await bot.send_message(config.levels_guide_id, text= f"{database.payout[user_id]};{user_id}", reply_markup=kb.admin_payout)
        await bot.send_message(user_id, f'Перевод: {database.payout[user_id]} рублей в процессе')
        # await message.answer(f'Вывод из liquid_wallet:\n - {database.payout[user_id]} рублей')
    except:
        await message.answer('Введите валидные реквизиты')
    await state.set_state(None)

@dp.callback_query(F.data == "admin_payout")
async def process_confirm_payment_button(callback_query: types.CallbackQuery, state: FSMContext) -> None: #message: Message, callback_query: types.CallbackQuery, 
    text = callback_query.message.text
    splitted = str(text).split(';')
    user_id = splitted[1]
    amount = splitted[0]
    user_id = int(user_id)
    database.payment_to_check_user_id = user_id
    amount = int(amount)
    await utils.add_liquid(user_id,(-1)*amount)
    await bot.send_message(config.levels_guide_id, text= f"прикрепляем чек USER (amount;ID)")
    await bot.edit_message_reply_markup(config.levels_guide_id, message_id=callback_query.message.message_id, reply_markup=None )
    await bot.send_message(user_id, f'Перевод исполнен:\n {amount} рублей' )
    await state.set_state(Form.admin_send_ckeck_state)

@dp.message(StateFilter(Form.admin_send_ckeck_state))
async def process_admin_send_ckeck_state(message: Message, state: FSMContext) -> None:
    await message.send_copy(database.payment_to_check_user_id)
    await state.set_state(None)





    
# @dp.message(StateFilter(Form.requisites_entering_state))
# async def process_requisites_entering_state(message: Message, state: FSMContext) -> None:


    

@dp.callback_query(F.data == "grow_wallet_up")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.grow_wallet_up)
    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'Grow: {user.grow_wallet} \nПополнить счёт. Введите сумму:')

@dp.message(StateFilter(Form.grow_wallet_up))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        if amount < 0: amount = -1*amount
        await state.set_state(None)
    except:
        await message.answer('Введите целое число')
    database.gamma[user_id] = amount
    
    # await utils.add_grow(user_id, int(amount))
    await message.answer(f'Пополнение grow_wallet:\n + {amount} рублей', reply_markup=kb.add_grow)


@dp.callback_query(F.data == "liquid_to_grow")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.liquid_to_grow)
    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'\nLiquid -> Grow\nДоступно Liquid: {user.liquid_wallet} \nВведите сумму:')

@dp.message(StateFilter(Form.liquid_to_grow))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        if amount < 0: amount = -1*amount
        if user.grow_wallet < int(amount):
            await message.answer(f'Недостаточно средств')
        else:
            await utils.add_liquid(user_id, (-1)*int(amount))
            await utils.add_grow(user_id, int(amount))
            await message.answer(f'\nLiquid -> Grow:\n{amount} рублей')
    except:
        await message.answer('Введите целое число')
    await state.set_state(None)
    

@dp.callback_query(F.data == "restate_up")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.restate_up)
    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'\nGrow -> Restate\n❗️Warning❗️\nRestate нельзя продать на уровне 0\nДоступно Grow: {user.grow_wallet} рублей\nВведите сумму:')

@dp.message(StateFilter(Form.restate_up))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        if amount < 0: amount = -1*amount
        if amount > user.grow_wallet:
            await message.answer(f'Недостаточно средств')
        else:
            await utils.add_grow(user_id, int(-1*amount))
            await utils.add_restate(user_id, int(amount))
            await message.answer(f'Пополнение restate:\n + {amount} рублей')
    except:
        await message.answer('Введите целое число')
    await state.set_state(None)
    
    
@dp.callback_query(F.data == "restate_down")
async def process_grow_to_liquid(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user = await database.get_user(user_id)
    await state.set_state(Form.restate_down)

    # await utils.up_liquid(user_id)
    await bot.send_message(user_id, f'Restate -> Grow\nКоммиссия 10%\nДоступно: {user.restate} рублей\nВведите сумму:')

@dp.message(StateFilter(Form.restate_down))
async def process_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    if user.level < 1:
        await bot.send_message(user_id, 'продажа недвижимости доступна с уровня 1')
    else:
        await state.update_data(amount=message.text)
        try:
            amount = int(message.text)
            if amount < 0: amount = -1*amount
            if user.restate < int(message.text):
                await message.answer(f'Недостаточно средств')
            else:
                await utils.add_restate(user_id, (-1)*int(amount))
                await utils.add_grow(user_id, (0.9)*int(amount))
                await message.answer(f'Вывод из restate:\n + {amount} рублей')
        except:
            await message.answer('Введите целое число')
        
    await state.set_state(None)

    
@dp.message(F.photo)
async def photo_handler(message: Message):
    await bot.send_message(message.from_user.id, f'вижу фото')
    photo_data = message.photo[-1]
    await bot.send_message(message.from_user.id, f'photo_data: {photo_data}')



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

switch_tabs_data =      ["menu"   , "profile"   , "resources"   , "level"      , "balance"    , "partners"    , "bonuses"   , "info"     ] 

switch_tabs_text=      ["Меню"   , "Профиль"   , "Ресурсы"     , "Уровень"    , "Баланс"     , "Партнеры"    , "Бонусы"    , "Инфо"     ]
switch_tabs_emoji_text=["📍\nМеню", "🪪\nПрофиль", "🔗\nРесурсы", "🔼\nУровень", "💳\nБаланс", "💎\nПартнеры", "🎁\nБонусы", "🔎\nИнфо"]
switch_tabs_commands = ["/menu"  , "/profile"  , "/resources"    , "/level"     , "/balance"   , "/partners"   , "/bonuses"    , "/info"    ]

@dp.callback_query(F.data)
async def swith_menu_tubs(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data in switch_tabs_data:

        await utils.switch_tubs(data, user_id=callback_query.from_user.id)
        # await bot.answer_callback_query(callback_query.from_user.id)

       
@dp.message(F.text)  
async def swith_menu_tubs(msg: Message):
    if msg.text in switch_tabs_emoji_text:
        index = switch_tabs_emoji_text.index(msg.text)

        data = switch_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    elif msg.text in switch_tabs_text:
        index = switch_tabs_text.index(msg.text)
        data = switch_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    elif msg.text in switch_tabs_commands:
        index = switch_tabs_commands.index(msg.text)
        data = switch_tabs_data[index]
        await utils.switch_tubs(data, user_id=msg.from_user.id)
    # await bot.answer_callback_query(callback_query.id)
        


