import random
import asyncio
import math 

import database
import utils
import texts
import kb
from misc import bot


from aiogram import types






async def get_user(user_id):
    # db = database.SessionLocal()
    # # user = await database.get_user(db, user_id)
    # user_name = "krosava"
    # referral_link = "https://nahuy"
    # referrer_id = 666
    # user = await database.get_or_create_user(user_name, referral_link, referrer_id, database.db,)
    user = await database.get_user(user_id)
    return  user
    
# def add_user(user_id, user_name, referral_link, referrer_id):
#     if user_id not in database.users:
#         time_now = datetime.now() + timedelta(hours=0, minutes=0)
   
#         database.users[user_id] = {"user_id":user_id, "user_name": user_name, "time_start": time_now, "level":  0, "restate": 0, "grow_wallet": 0, "liquid_wallet": 0, "turnover": 0,\
#             "sales": 0, "bonuses_available": 0, "bonuses_gotten": 0, "guide_stage": 0, "current_leader_id": referrer_id, "referrers": [referrer_id], "referrals": [], "referral_link": referral_link, "bonus_cd": time_now}


# async def get_balance_sum(user_id):
#     user  = await get_user(user_id)
#     balance_sum = user.restate + user.grow_wallet + user.liquid_wallet 
#     return balance_sum

# BONUS
async def add_bonus(user_id):
    # user = await get_user(user_id)
    try:
        # current_user = database.db.query(database.User).filter(database.User.user_id == user_id).first()
        # await bot.send_message(user_id,"get_user: Пользователь найден")
        # current_user.bonuses_gotten+= 1
        # current_user.bonuses_available+= 1
        # db = database.SessionLocal()
        user = database.local_users[user_id] 
        # await bot.send_message(user_id, 'Сейчас выдам первый бонус')
        user.bonuses_gotten += 1
        user.bonuses_available += 1
        # db.refresh(user)
        db = database.SessionLocal()
        record = db.merge(database.User( ))
        # await bot.send_message(user_id, 'проверяй')
    except:
         await bot.send_message(user_id, 'Пользователь не найден.\nПожалуйста, войдите по реферальной ссылке')
    # user.bonuses_gotten += 1
    # user.bonuses_available += 1
         
async def up_level(user_id):
    user = database.local_users[user_id] 
    next_level = (user.level)+1
    restate_require = database.ubicoin * (2 ** (next_level))
    lead_grace = database.ubicoin * (2 ** (next_level))
    balance = user.restate + user.grow_wallet + user.liquid_wallet
    # delta = (lead_grace + restate_require) - balance
    # gamma = lead_grace - (user.grow_wallet+user.liquid_wallet)
    if (restate_require-user.restate) > 0:
        gamma = lead_grace-(user.grow_wallet + user.liquid_wallet-(restate_require-user.restate)) 
    else:  
         gamma = lead_grace-(user.grow_wallet + user.liquid_wallet)

    if gamma > 0:
        # await bot.send_message(user_id,  f'gamma: {gamma}, gamma2: {(math.ceil(gamma/100)*100)}')
        database.gamma = math.ceil(gamma/100)*100
        await bot.send_message(user_id, f'Следующий уровень: {next_level}\n\nRestate: {restate_require} руб\nСпасибо Лиду: {lead_grace} руб' +'\n\n\
            Баланс: '+ '%.2f' %(balance) + " руб"+ f'\n\nПополните баланс на {database.gamma} руб', reply_markup=kb.add_balance)
    else:
        await bot.send_message(user_id, f'На следующий уровень: {next_level}\nМожно перейти с Restate: {restate_require} руб\nБлагодарность Лиду: {lead_grace} руб' +'\n\n\
            Баланс: '+ '%.2f' %(balance) + " руб", reply_markup=kb.up_me)

async def add_balance(user_id):
    # user = database.local_users[user_id] 
    await bot.send_message(user_id, f'Пополнение баланса:\n\n + {database.gamma} рублей\n\nТинькофф СБП: +7(996)893-15-12\n\nТелеграм TON:\nUQAegScNLWtuhtDlBd2oq5Utjkm_W_NSmWlBvYU83z65uMu7\
        \n\nПосле перевода нажмите кнопку готово\nИ отправьте боту чек\n\nПлатежи пока подтверждает кожан... хм... человек\nЕсли он не уложится в 6 часов 😴\nМы добавим вам на счёт\
                           10% от суммы перевода (вычтем у него из зарплаты) ', reply_markup=kb.add_balance_ready)

async def add_balance_ready(user_id):
    user = database.local_users[user_id]
    user.liquid_wallet+=database.gamma
    db = database.SessionLocal()
    record = db.merge(database.User( )) 
    await bot.send_message(user_id, f'Баланс пополнен: {database.gamma} рублей\n\nПравило успешных: чем больше отдаёшь, тем больше получаешь. Проверили. Работает.')


async def up_me(user_id):
    user = database.local_users[user_id]
    restate_require = database.ubicoin * (2 ** (user.level+1))
    lead_grace = database.ubicoin * (2 ** (user.level+1))
    # balance = user.restate + user.grow_wallet + user.liquid_wallet
    # if balance > (lead_grace+restate_require):
    #    
    if (restate_require-user.restate) > 0:
       gamma = lead_grace-(user.grow_wallet + user.liquid_wallet-(restate_require-user.restate)) 
    else:  
        gamma = lead_grace-(user.grow_wallet + user.liquid_wallet)
    if gamma > 0:
        await bot.send_message(user_id,  f'Недостаточно средств: {gamma} рублей')
    else:
        if restate_require > user.restate:
            user.grow_wallet-=(restate_require-user.restate)
            user.restate=restate_require
        user.grow_wallet-=lead_grace
        if user.grow_wallet < 0:
            user.liquid_wallet+=user.grow_wallet
            user.grow_wallet=0
        user.level += 1
        db = database.SessionLocal()
        record = db.merge(database.User( )) 
    await bot.send_message(user_id, f'Ваш уровень: {user.level}\n')


async def get_bonuses_available(user_id):
    user = await database.get_user(user_id)
    bonuses_available = user.bonuses_available
    return bonuses_available

async def get_bonuses_gotten(user_id):
    user = await get_user(user_id)
    return user.bonuses_gotten


async def open_bonus(user_id):
    user = await database.get_user(user_id)
    if user.bonuses_available >= 1:
        user.bonuses_available-= 1
        bonus_size = float(random.randint(0, 251))
        bonus_size = bonus_size / 100
        bonus_size = bonus_size ** 4
        bonus_size = bonus_size + 10.31
        user.restate += bonus_size
        user.turnover += bonus_size
        db = database.SessionLocal()
        record = db.merge(database.User( ))
        bonuses_gotten = user.bonuses_gotten
        balance_sum = user.restate+user.grow_wallet+user.liquid_wallet
        text1 = '🔼 Получено бонусов:     ' + f"{bonuses_gotten}"
        text2 = f"\n🎁 Бонус:         " + '%.2f' %(bonus_size) + " рублей" 
        text3 = "\n💳 Баланс:      " + ( '%.2f' %(balance_sum)) + " рублей"
        await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'), caption=text1 + text2 + text3)
    else:
        await bot.send_video(user_id, video=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\\videos\\travolta.gif.mp4'), caption="\
        Здесь пока ничего нет. Куда всё делось? 🤔 \n\nБонусы разыгрываются каждый день! \nМы отправим уведомление, когда придет бонус.\
                            \n\nРекомендуем включить всплывающие уведомления в настройках бота🔔 Чтобы не пропустить.\n\n Нажимайте поделиться\n получайте бонус за каждого нового подписчика! 🎁") 


# START Guide Stages
async def start_guide_stages(user_id):
    user = await database.get_user(user_id)

    if user.guide_stage  == 0:
        await utils.start_guide1(user_id)

    elif user.guide_stage  == 1:
        await utils.start_guide2(user_id)

    elif user.guide_stage == 2:
        await utils.start_guide3(user_id)

    elif user.guide_stage  == 3:
        await utils.start_guide4(user_id)

    elif user.guide_stage  >= 4:
            await utils.main_menu(user_id)


async def get_balance(user_id):
    # if await utils.get_user(user_id) == False:
    #      await bot.send_message(user_id, "Пользователь не найден. Перезагрузите бота")
    # else:     
        user = await get_user(user_id)

        text1 = "\n\n1️⃣ Restate(25%):             " + '%.2f' %(user.restate) + ' рублей'
        text2 = "\n2️⃣ Grow(20%):               " + '%.2f' %(user.grow_wallet) + ' рублей'
        text3 = "\n3️⃣ Liquid(0%):                  " + '%.2f' %(user.liquid_wallet) + ' рублей'
        sum = user.restate + user.grow_wallet + user.liquid_wallet
        text0 = "💳 Баланс:                       " + ( '%.2f' %(sum)) + " рублей"
        balance = text0 + text1 + text2 + text3 + texts.accounts_about_text
        await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\Clone_git\levels_tg_bot\BASE_MEDIA\pics\\restate_grow_liquid.jpg'), caption=f'{balance}', reply_markup=kb.balance_markup)
      
# TABS вкладки
#  Вкладки МЕНЮ
async def main_menu(user_id):
     await bot.send_message(user_id, "🔴 Кнопки внизу 🔢 ⬇️", reply_markup=kb.menu_buttons_reply_markup)
    #  await bot.send_message(user_id, " Все  вкладки  главного  меню  ", reply_markup=kb.menu_markup)

async def profile_tub(user_id):
    user_info_text = "🪪 Профиль\n\n" + await database.user_info( user_id)
    await bot.send_message(user_id, user_info_text, disable_web_page_preview=True, reply_markup=kb.profile_markup)

async def level_tub(user_id):
    user = await utils.get_user(user_id)
    level = user.level
    leader_id = user.current_leader_id
    try:
        current_leader = await utils.get_user(leader_id)
        leader_name = current_leader.user_name
        leader_level=current_leader.level
        await bot.send_message(user_id, f"\nВаш уровень: {level}"+f'\n\nВаш ЛИД сейчас:\n{leader_name}\nLevel: {leader_level}', reply_markup=kb.level_markup)
    except:
        await bot.send_message(user_id, f"\nВаш уровень: {level}", reply_markup=kb.level_markup)

async def balance_tub(user_id):
    await get_balance(user_id)

async def partners_tub(user_id):
    user = await utils.get_user(user_id)
    referrals = user.referrals 
    leader_id = user.current_leader_id
    try:
        current_leader = await utils.get_user(leader_id)
        leader_name = current_leader.user_name
        leader_level=current_leader.level
        await bot.send_message(user_id, "💎 Партнеры" +f'\n\nВаш ЛИД сейчас:\n{leader_name}\nLevel: {leader_level} ' 
        + "\n\nНаставники доступны: " + f"\n\nВаши рефералы: {referrals}", reply_markup=kb.partners_markup)
    except:
        await bot.send_message(user_id, "💎 Партнеры" +f'\n\nВаш ЛИД не найден' 
            + f"\n\n\nВаши рефералы: {referrals}", reply_markup=kb.partners_markup)

async def bonuses_tub(user_id):
    user = await database.get_user(user_id)
    bonuses_available = user.bonuses_available
    bonuses_gotten = user.bonuses_gotten
    if await utils.get_user(user_id) == False:
        await bot.send_message(user_id, "Пользователь не найден. Перезагрузите бота")
    else:   
        referral_link = user.referral_link 
        text2 = f"\n\nВаша личная реф ссылка:\n{referral_link}"
        await bot.send_message(user_id, texts.bonuses_tub_text1 + text2 + texts.bonuses_tub_text2 + f"{bonuses_gotten}"\
                                + "\nДоступно бонусов: " + f"{bonuses_available}", reply_markup=kb.bonuses_markup)
        
async def resources_tub(user_id):
    resurses_text = '\n\nОфициальный канал: https://t.me/Levels_up'
    await bot.send_message(user_id, "🔗 Ресурсы" + resurses_text, reply_markup=kb.resources_markup)

async def info_tub(user_id):
    await bot.send_message(user_id, "🔎 Инфо"+ texts.info_text, reply_markup=kb.info_markup)

async def switch_tubs(code , user_id):
    if code == "menu":
        await utils.main_menu(user_id)
    elif code == "profile":
        await utils.profile_tub(user_id)
    elif code == "resources":
        await utils.resources_tub(user_id)
    elif code == "level":
        await utils.level_tub(user_id)
    elif code == "balance":
        await utils.balance_tub(user_id)
    elif code == "partners":
        await utils.partners_tub(user_id)
    elif code == "bonuses":
        await utils.bonuses_tub(user_id)
    elif code == "info":
        await utils.info_tub(user_id)
# Guide
# Про Уровни. Даем первый бонус. Открывайте.
async def start_guide1(user_id):
    await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\choose_your_level2.jpg.jpg'),caption=texts.start_guide1_text)
    await asyncio.sleep(1)
    # user = await utils.get_user(user_id)
    # utils.get_user(user_id).guide_stage  = 1
    user = database.local_users[user_id]
    user.guide_stage  = 1
    if user.bonuses_gotten  == 0:
         await utils.add_bonus(user_id)
    elif user.bonuses_gotten  >= 1:
            await bot.send_message(user_id, 'Хм...\nКажется, вы уже получили первый бонус')
    db = database.SessionLocal()
    record = db.merge(database.User())
    await bot.send_message(user_id,"Начнем с небольшого бонуса", reply_markup=kb.bonus_button)

# Открывам бонус 1. Про бонусы. Для второго бонуса - подписка на канал
async def start_guide2(user_id):
    await asyncio.sleep(1)
    await bot.send_message(user_id, "Сначала бонусы могут содежать\nот 10 до 50 рублей.\n\nДальше - больше 🔼")
    await asyncio.sleep(1)
    await bot.send_message(user_id, "Можно получить следующий бонус за 2 простых действия:")
    await asyncio.sleep(1)
    await bot.send_message(user_id, "1. Подписка на канал", reply_markup=kb.subscribe_buttons)
    # utils.get_user(user_id).guide_stage = 2
    user = database.local_users[user_id]
    user.guide_stage  = 2
    db = database.SessionLocal()
    record = db.merge(database.User( ))

# Поделиться своей реферальной ссылкой в ТГ.
async def start_guide3(user_id):  
        user = database.local_users[user_id]
        user_channel_status = await bot.get_chat_member(chat_id='-1001973511610', user_id=user_id)
        if user_channel_status != 'left':
            if user_channel_status.status == "creator" or user_channel_status.status == "member" or user_channel_status.status == 'ChatMemberMember':
                # utils.get_user(user_id).guide_stage  = 3
                user.guide_stage  = 3
                if user.bonuses_gotten  == 1:
                    await utils.add_bonus(user_id)
                elif user.bonuses_gotten  >= 2:
                    await bot.send_message(user_id, 'Хм...\nКажется, вы уже получили 2 бонуса')
                await bot.send_message(user_id, 'Спасибо за подписку')
                await bot.send_message(user_id, '2. Поделиться СВОЕЙ реферальной ссылкой в ТГ.')
                await asyncio.sleep(2)
                referral_link = user.referral_link 
                await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'),\
                            caption= texts.start_guide3_text_1 +f"{referral_link}" + "\n🎁 ⬆️ Бонус здесь ⬆️ 🎁\n\n❗️ ♻️ 🔁 РЕПОСТ тут ➡️ ➡️ ➡️")
                await asyncio.sleep(2)
                await bot.send_message(user_id, texts.start_guide3_text_2, reply_markup=kb.check_done_button)
            else:
                await bot.send_message(user_id, 'Нет подписки. Можно продолжить без подписки и потерять следующий бонус 😱', reply_markup=kb.subscribe_buttons2)
        db = database.SessionLocal()
        record = db.merge(database.User( ))


# Без подписки на канал нет бонус
async def start_guide3_nosub(user_id):
    user = database.local_users[user_id]
    user.guide_stage  = 3
    if user.bonuses_gotten == 1:
                    user.bonuses_gotten = 2
    await bot.send_message(user_id, '☹️')
    await bot.send_message(user_id, '2. Поделиться своей реферальной ссылкой в ТГ.')
    await asyncio.sleep(2)
    referral_link = user.referral_link 
    await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'),\
                caption= texts.start_guide3_text_1 + f"{referral_link}" + "\n🎁 ⬆️ Бонус здесь ⬆️ 🎁\n\n❗️ ♻️ 🔁 РЕПОСТ тут ➡️ ➡️ ➡️")
    await asyncio.sleep(2)
    await bot.send_message(user_id, texts.start_guide3_text_2, reply_markup=kb.check_done_button)
    db = database.SessionLocal()
    record = db.merge(database.User( ))


async def start_guide3_1(user_id):
    await bot.send_message(user_id, 'OK')
    await asyncio.sleep(1)
    await bot.send_message(user_id, 'А вот и бонус!', reply_markup=kb.bonus_button)


async def start_guide4(user_id):
    user = database.local_users[user_id]
    user.guide_stage  = 4
    await asyncio.sleep(1)
    await bot.send_message(user_id, texts.start_guide4_text, disable_web_page_preview=True)
    await asyncio.sleep(2)
    await bot.send_message(user_id, texts.start_guide4_text_2, reply_markup=kb.menu_button_markup)
    db = database.SessionLocal()
    record = db.merge(database.User( ))



