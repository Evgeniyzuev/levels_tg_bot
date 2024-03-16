import random
import pickle
import database
import utils
import texts
import kb
import asyncio
from datetime import datetime, timedelta

from aiogram import types 
# from aiogram import Bot, F, Router, flags
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, InputFile
# from aiogram.filters import Command
# from aiogram.enums.parse_mode import ParseMode
# from database import SessionLocal, User

from misc import bot
db = database.SessionLocal()



def get_user(user_id):
    if user_id not in database.users:
    # if not db.users(user_id):
         return False
    else:
          return database.users[user_id]
    
def add_user(user_id, user_name, referral_link, referrer_id):
    if user_id not in database.users:
        time_now = datetime.now() + timedelta(hours=0, minutes=0)
   
        database.users[user_id] = {"user_id":user_id, "user_name": user_name, "time_start": time_now, "level":  0, "real_estate": 0, "grow_wallet": 0, "liquid_wallet": 0, "turnover": 0,\
            "sales": 0, "bonuses_available": 0, "bonuses_gotten": 0, "guide_stage": 0, "current_leader_id": referrer_id, "referrers": [referrer_id], "referrals": [], "referral_link": referral_link, "bonus_cd": time_now}


def get_balance_sum(user_id):
    user = user = get_user(user_id)
    balance_sum = user["real_estate"] + user["grow_wallet"] + user["liquid_wallet"]
    return balance_sum

# BONUS
def add_bonus(user_id):
    user = get_user(user_id)
    user["bonuses_gotten"] += 1
    user["bonuses_available"] += 1

def get_bonuses_available(user_id):
    user = get_user(user_id)
    return user["bonuses_available"]

def get_bonuses_gotten(user_id):
    user = get_user(user_id)
    return user["bonuses_gotten"]

async def open_bonus(user_id):
    user = get_user(user_id)
    if user["bonuses_available"] >= 1:
        user["bonuses_available"] -= 1
        bonus_size = float(random.randint(0, 251))
        bonus_size = bonus_size / 100
        bonus_size = bonus_size ** 4
        bonus_size = bonus_size + 10.31
        user["real_estate"] += bonus_size
        user["turnover"] += bonus_size
        bonuses_gotten = utils.get_bonuses_gotten(user_id)
        text1 = '🔼 Получено бонусов:     ' + f"{bonuses_gotten}"
        text2 = f"\n🎁 Бонус:         " + '%.2f' %(bonus_size) + " рублей\n" 
        text3 = "💳 Баланс:      " + ( '%.2f' %(utils.get_balance_sum(user_id=user_id))) + " рублей"
        await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'), caption=text1 + text2 + text3)
    else:
        await bot.send_video(user_id, video=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\\videos\\travolta.gif.mp4'), caption="\
        Здесь пока ничего нет. Куда всё делось? 🤔 \n\nБонусы разыгрываются каждый день! \nМы отправим уведомление, когда придет бонус.\
                            \n\nРекомендуем включить всплывающие уведомления в настройках бота🔔 Чтобы не пропустить.\n\n Нажимайте поделиться\n получайте бонус за каждого нового подписчика! 🎁") 


# START Guide Stages
async def start_guide_stages(user_id):

    if utils.get_user(user_id)["guide_stage"] == 0:
        await utils.start_guide1(user_id)

    elif utils.get_user(user_id)["guide_stage"] == 1:
        await utils.start_guide2(user_id)

    elif utils.get_user(user_id)["guide_stage"] == 2:
        await utils.start_guide3(user_id)

    elif utils.get_user(user_id)["guide_stage"] == 3:
        await utils.start_guide4(user_id)

    elif utils.get_user(user_id)["guide_stage"] >= 4:
            await utils.main_menu(user_id)


async def get_balance(user_id):
    if utils.get_user(user_id) == False:
         await bot.send_message(user_id, "Пользователь не найден. Перезагрузите бота")
    else:     
        user = get_user(user_id)
        text0 = "💳 Баланс:                      " + ( '%.2f' %(utils.get_balance_sum(user_id=user_id))) + " рублей"
        text1 = "\n\n1️⃣ Restate(25%):             " + '%.2f' %(user["real_estate"]) + ' рублей'
        text2 = "\n2️⃣ GROW(20%):               " + '%.2f' %(user["grow_wallet"]) + ' рублей'
        text3 = "\n3️⃣ Liquid(0%):                  " + '%.2f' %(user["liquid_wallet"]) + ' рублей'
        balance = text0 + text1 + text2 + text3 + texts.accounts_about_text
        await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\real_estate_trees_lake.jpg'), caption=balance, reply_markup=kb.balance_markup )

# TABS вкладки
#  Вкладки МЕНЮ
async def main_menu(user_id):
     await bot.send_message(user_id, " 📍    Меню    ", reply_markup=kb.menu_buttons_reply_markup)
    #  await bot.send_message(user_id, " Все  вкладки  главного  меню  ", reply_markup=kb.menu_markup)

async def profile_tub(user_id):
    user = get_user(user_id)
    level = user["level"]
    turnover = user["turnover"]
    sales = user["sales"]
    referral_link = user["referral_link"]
    text = "🪪 Профиль" + f"\nВаш уровень: {level}"
    text1 = "\n\nВесь оборот:   " + '%.2f' %(turnover) + ' рублей'
    text2 = f"\nВсего продаж:    {sales}"
    text3 = f"\n\nВаша личная реф ссылка: {referral_link}"
    await bot.send_message(user_id, text + text1 + text2, reply_markup=kb.profile_markup)

async def level_tub(user_id):
    level = utils.get_user(user_id)["level"]
    await bot.send_message(user_id, "🔼 Уровень" + f"\nВаш уровень: {level}", reply_markup=kb.resources_markup)
async def balance_tub(user_id):
    await get_balance(user_id)

async def partners_tub(user_id):
    referrals = utils.get_user(user_id)["referrals"]
    await bot.send_message(user_id, "💎 Партнеры"+ f"\nВаши рефералы: {referrals}", reply_markup=kb.partners_markup)

async def bonuses_tub(user_id):
    if utils.get_user(user_id) == False:
        await bot.send_message(user_id, "Пользователь не найден. Перезагрузите бота")
    else:   
        referral_link = utils.get_user(user_id)["referral_link"]
        text2 = f"\n\nВаша личная реф ссылка:\n{referral_link}"
        await bot.send_message(user_id, texts.bonuses_tub_text1 + text2 + texts.bonuses_tub_text2 + f"{utils.get_bonuses_gotten(user_id)}"\
                                + "\nДоступно бонусов: " + f"{utils.get_bonuses_available(user_id)}", reply_markup=kb.bonuses_markup)
        
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
    utils.get_user(user_id)["guide_stage"] = 1
    if utils.get_user(user_id)["bonuses_gotten"] == 0:
                utils.add_bonus(user_id)
    elif utils.get_user(user_id)["bonuses_gotten"] >= 1:
            await bot.send_message(user_id, 'Хм...\nКажется, вы уже получили первый бонус')
    
    await bot.send_message(user_id,"Начнем с небольшого бонуса", reply_markup=kb.bonus_button)

# Открывам бонус 1. Про бонусы. Для второго бонуса - подписка на канал
async def start_guide2(user_id):
    # await utils.open_bonus(user_id)
    await asyncio.sleep(1)
    await bot.send_message(user_id, "Сначала бонусы могут содежать\nот 10 до 50 рублей.\n\nДальше - больше 🔼")
    await asyncio.sleep(1)
    await bot.send_message(user_id, "Можно получить следующий бонус за 2 простых действия:")
    await asyncio.sleep(1)
    await bot.send_message(user_id, "1. Подписка на канал", reply_markup=kb.subscribe_buttons)
    utils.get_user(user_id)["guide_stage"] = 2

# Поделиться своей реферальной ссылкой в ТГ.
async def start_guide3(user_id):  
    #  if utils.get_user(callback_query.from_user.id,)["guide_stage"] == 2:
        user_channel_status = await bot.get_chat_member(chat_id='-1001973511610', user_id=user_id)
        if user_channel_status != 'left':
            if user_channel_status.status == "creator" or user_channel_status.status == "member" or user_channel_status.status == 'ChatMemberMember':
                utils.get_user(user_id)["guide_stage"] = 3
                if utils.get_user(user_id)["bonuses_gotten"] == 1:
                    utils.add_bonus(user_id)
                elif utils.get_user(user_id)["bonuses_gotten"] >= 2:
                    await bot.send_message(user_id, 'Хм...\nКажется, вы уже получили 2 бонуса')
                await bot.send_message(user_id, 'Спасибо за подписку')
                await bot.send_message(user_id, '2. Поделиться СВОЕЙ реферальной ссылкой в ТГ.')
                await asyncio.sleep(2)
                referral_link = utils.get_user(user_id)["referral_link"]
                await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'),\
                            caption= texts.start_guide3_text_1 +f"{referral_link}" +"\n🎁 Бонус здесь⬆️   🔁РЕПОСТ тут➡️")
                await asyncio.sleep(2)
                await bot.send_message(user_id, texts.start_guide3_text_2, reply_markup=kb.check_done_button)
            else:
                await bot.send_message(user_id, 'Нет подписки. Можно продолжить без подписки и потерять следующий бонус 😱', reply_markup=kb.subscribe_buttons2)

# Без подписки на канал нет бонус
async def start_guide3_nosub(user_id):

    utils.get_user(user_id)["guide_stage"] = 3
    if utils.get_user(user_id,)["bonuses_gotten"] == 1:
                    utils.get_user(user_id,)["bonuses_gotten"] = 2
    await bot.send_message(user_id, '☹️')
    await bot.send_message(user_id, '2. Поделиться своей реферальной ссылкой в ТГ.')
    await asyncio.sleep(2)
    referral_link = utils.get_user(user_id)["referral_link"]
    await bot.send_photo(user_id, photo=types.FSInputFile('D:\Git\levels_tg_bot\levels_tg_bot\BASE_MEDIA\pics\\bonus_open.jpg'),\
                caption= texts.start_guide3_text_1 + f"{referral_link}" + "\n🎁 Бонус здесь⬆️   🔁РЕПОСТ тут➡️")
    await asyncio.sleep(2)
    await bot.send_message(user_id, texts.start_guide3_text_2, reply_markup=kb.check_done_button)

async def start_guide3_1(user_id):
    await bot.send_message(user_id, 'OK')
    await asyncio.sleep(1)
    await bot.send_message(user_id, 'А вот и бонус!', reply_markup=kb.bonus_button)


async def start_guide4(user_id):
    utils.get_user(user_id)["guide_stage"] = 4
    # await utils.open_bonus(user_id)
    await asyncio.sleep(1)
    await bot.send_message(user_id, texts.start_guide4_text, disable_web_page_preview=True)
    await asyncio.sleep(2)
    await bot.send_message(user_id, texts.start_guide4_text_2, reply_markup=kb.menu_button_markup)



