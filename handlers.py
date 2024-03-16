import kb
import texts
import utils
import database #import SessionLocal, User
from datetime import datetime, timedelta

from aiogram import types, F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from sqlalchemy.sql import func

from misc import dp, bot
from states import Gen

# START
# @dp.message(Command("start"))
@dp.message(CommandStart(deep_link=True))
async def start_handler(message: Message , command: CommandObject):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    try:
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
    if referrer_id == user_id:
        try:
            await bot.send_message(user_id, text='❗️ Вы зашли по своей ссылке ❗️')
        finally:
            pass        

    if utils.get_user(user_id) == False:
        referral_link = await create_start_link(bot,str(message.from_user.id), encode=True)
        utils.add_user(user_id, user_name, referral_link, referrer_id)
        # referrer_name = utils.get_user(user_id)["referrer_name"]

    try:
        await bot.send_message(user_id, text=f'ВНИМАНИЕ❗️❗️❗️\nБот работает в тестовом режиме\n❗️Никаких выплат не будет до релиза\nРепосты делайте на свой страх и риск')
        await bot.send_message(referrer_id, text= f"По вашей ссылке зашел пользователь:\n{user_name}. ID: {user_id} \nВы получите бонус 🎁 когда пользователь откроет два бонуса.")
    finally:
        pass 


 # TRRRRRYYYY DATABASE
    # TRRRRRYYYY DATABASE
    db = database.SessionLocal()

    try:
        referrer = await database.get_user(db, referrer_id)
        # if user.referrer:
        #         user.referrer.referred.append(user)
        #         # await notify_referrer(db, user.referrer, user)
        db.commit()
        await message.answer(f"Вас пригласил {referrer.user_name}")
    except:
        await message.answer(f"Кто вас пригласил?")

    referral_link = await create_start_link(bot,str(message.from_user.id), encode=True)
    user = await  database.get_or_create_user(db, message.from_user.id, message.from_user.username, referral_link, referrer_id)
    # user =await database.get_user (db, message.from_user.id) 


    
    user_info_text = await database.user_info(db, user_id)

    await message.answer(user_info_text)















    # db = database.SessionLocal()
    # await  database.create_user(db, message.from_user.id, message.from_user.username, referral_link, referrer_id)
    # try:
    #     referrer = await database.get_user(db, referrer_id)
    #     # if user.referrer:
    #     #         user.referrer.referred.append(user)
    #     #         # await notify_referrer(db, user.referrer, user)
    #     db.commit()
    #     await message.answer(f"Вас пригласил {referrer.user_name}")
    # except:
    #     await message.answer(f"Кто вас пригласил?")
    # referral_link = await create_start_link(bot,str(message.from_user.id), encode=True)

    

   


    # # await message.answer(f"Registration Successful\nuser_id: {user.user_id}\nuser_name: {user.user_name}\nreferral_link: {user.referral_link}\nregistration_time:" )

    # text = await  database.user_info(db, message.from_user.id)
    # await message.answer(text)

    # await message.answer(f"Registration Successful\nuser_id: {user.user_id}\nuser_name: {user.user_name}\nreferral_link: {user.referral_link}")


    # try:
    #     user = await database.get_or_create_user(db, message.from_user.id, message.from_user.username, referral_link, referrer_id)
    #     # registration_time = f" {user.registration_time}"

    #     # user_info = f'Registration Successful\nuser_id: {user.user_id}'



    #     # user_info = (f"Registration Successful\nuser_id: {user.user_id}
    #     # \nuser_name: {user.user_name}\nreferral_link: {user.referral_link} \nregistration_time:\ # {user.registration_time}\ 
    #     # \nlevel: {user.level}\nreal_estate: {user.real_estate}\ngrow_wallet: {user.grow_wallet}\nliquid_wallet: {user.liquid_wallet}\nturnover: {user.turnover}\nsales: {user.sales}\
    #     # \nbonuses_available: {user.bonuses_available}\nbonuses_gotten: {user.bonuses_gotten}\nguide_stage: {user.guide_stage}\ncurrent_leader_id: {user.current_leader_id}\nreferrers: {user.referrers}\
    #     # \nreferrals: {user.referrals}\nbonus_cd_time: {user.bonus_cd_time}")
    #     # await bot.send_message(user_id,  user_info)
    #     user_info = await database.user_info(db, message.from_user.id)
    #     await message.answer(user_id,user_info)
    # except:
    #     await message.answer(user_id,"user_info")
    #     pass



    # try:
    #     referrer = await database.get_user(db, referrer_id)
    #     db.commit()
    # # if user.referrer:
    # #         user.referrer.referred.append(user)
    # #         # await notify_referrer(db, user.referrer, user)
    #     await message.answer(f"Вас пригласил {referrer.user_name}")
    # except:
    #     await message.answer(f"Кто вас пригласил?")
    #     pass


    
    


    # user = User(user_id=user_id, user_name=user_name, referral_link=referral_link, referrer_id=referrer_id, registration_time=time_now, level=0, real_estate=0, grow_wallet=0, liquid_wallet=0, turnover=0,\
    # sales=0, bonuses_available=0, bonuses_gotten=0, guide_stage=0, current_leader_id=referrer_id, referrers=referrers_text, referrals = '', bonus_cd_time = time_now     )






    # async with SessionLocal() as db:
    # async with SessionLocal() as db:
    #     db = SessionLocal()
    #     user = await get_or_create_user(db, message.from_user.id, message.from_user.username, referrer_id)
    #     if user.referrer:
    #         user.referrer.referred.append(user)
    #         await db.commit()
    # await message.answer(f"Hello, {message.from_user.first_name}! Your referral link is <a href='tg://user?id={user.id}'>t.me/{user.username}</a>")

    # async def get_or_create_user(db, user_id, username, referrer_id):
    #     user = await db.query(User).filter(User.id == user_id).first()
    #     if not user:
    #         user = User(id=user_id, username=username)
    #         db.add(user)
    #         await db.commit()
    #         await db.refresh(user)
    #         if referrer_id:
    #             referrer = await db.query(User).filter(User.id == referrer_id).first()
    #             if referrer:
    #                 user.referrer_id = referrer.id
    #                 referrer.subscribers.append(user)
    #     return user

    await utils.start_guide_stages(user_id)



# Нажатие кнопки открыть бонус
@dp.callback_query(F.data == "open_bonus")
async def process_open_bonus_button(callback_query: types.CallbackQuery): 
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    bonuses_gotten = utils.get_user(user_id)["bonuses_gotten"]
    bonuses_available = utils.get_user(user_id)["bonuses_available"]
    if bonuses_available > 0:
        if bonuses_gotten-bonuses_available == 1:
            try:
                current_leader_id = utils.get_user(user_id)["current_leader_id"]
                await bot.send_message(current_leader_id, text= f"Ваш реферал: {user_name}(ID: {user_id}) открыл второй бонус.", reply_markup=kb.get_and_open_bonus_button)
            except:
                await bot.send_message(user_id, text="не получилось")   
    await utils.open_bonus(user_id)
    if utils.get_user(user_id)["guide_stage"] == 1:
        await utils.start_guide2(user_id)  
    elif utils.get_user(user_id)["guide_stage"] == 3:
        await utils.start_guide4(user_id)

# Нажатие кнопки получать бонус за реферала
@dp.callback_query(F.data == "get_and_open_bonus")
async def process_get_and_open_bonus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.edit_message_reply_markup(user_id, message_id=callback_query.message.message_id, reply_markup=None )
    utils.add_bonus( user_id )
    await bot.send_message(user_id, text="+🎁 Бонус получен!\nОткройте его на вкладке Бонусы")

@dp.callback_query(F.data == "check_subscribe_button")
async def check_subs(callback_query: types.CallbackQuery):
    # if utils.get_user(callback_query.from_user.id)["guide_stage"] == 2:
        user_id = callback_query.from_user.id
        await utils.start_guide3(user_id)    
    
@dp.callback_query(F.data == "no_subscribtion")
async def check_subs(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if utils.get_user(user_id)["guide_stage"] == 2:
        await utils.start_guide3_nosub(user_id) 

@dp.callback_query(F.data == "check_done_button")
async def check_done(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if utils.get_user(user_id)["guide_stage"] == 3:
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
        


