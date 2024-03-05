import kb
import text
import utils
import db

from aiogram import types, F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from misc import dp, bot
from states import Gen

# START
@dp.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.reply_markup)
    await msg.answer("MENU", reply_markup=kb.menu_markup)

# MENU
@dp.message(F.text == "📍Меню")
@dp.message(F.text == "/menu")  
async def process_menu_button(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_markup)

# BONUS
@dp.callback_query(F.data == "get_bonus")
async def process_get_bonus_button(callback_query: types.CallbackQuery): 
    if (db.bonuses_available > 0): 
        utils.bonus_open()
        msg = "бонус получен: " + ( '%.2f' %(db.bonus_size/100)) + " рублей\n" + "Баланс: " + ( '%.2f' %(utils.get_balance()/100)) + " рублей"
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, msg)
    else:
        msg = "Получите бонус за каждого вашего подписчика\
        \n\nБонусы разыгрываются каждый день! \nМы отправим уведомление, когда придет бонус."
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, msg, reply_markup=kb.share_button)

@dp.message(F.text == "🎁Бонусы")  
async def process_get_bonus_button(msg: Message):
    await msg.answer("Доступно бонусов: " + str(db.bonuses_available), reply_markup=kb.bonus_button)

@dp.callback_query(F.data == "bonuses")
async def process_get_bonus_button(callback_query: types.CallbackQuery):
    msg = "Доступно бонусов: " + str(db.bonuses_available)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg, reply_markup=kb.bonus_button)

# SHARE
@dp.callback_query(F.data == "share")
async def process_share_button(callback_query: types.CallbackQuery):
    db.bonuses_available += 1
    msg = "Вы получили бонус!"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg)


#PROFILE
@dp.callback_query(F.data == "profile")
async def process_profile_button(callback_query: types.CallbackQuery):
    msg = "Ваш профиль "
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg)

#BALANCE

@dp.callback_query(F.data == "balance")
@dp.message(F.text == "💳Баланс")
@dp.message(F.text == "/balance")  
async def me_balance_button(msg: Message):
    text_balance = "НЕДВИЖИМОСТЬ(25%): " + ( '%.2f' %(db.real_estate/100)) + "рублей" +\
    "\n\nРостсчет(20%): " + ( '%.2f' %(db.grow_wallet/100)) + "рублей" +\
    "\n\nКошелек(0%): " + ( '%.2f' %(db.liquid_wallet/100)) + "рублей"
    await msg.answer(text_balance, reply_markup=kb.transfer_button)

# @dp.callback_query(F.data == "balance")




@dp.message(Command("1"))
async def process_1_command(message: types.Message):
    await message.answer("inline 1", reply_markup=kb.iexit_kb)


# @dp.message(lambda message: message.text in ['hi4'])
# async def process_hi4_command(message: types.Message):
#     await message.reply("Четвертое - расставляем кнопки в ряд", reply_markup=kb.markup1)
# # async def message_handler(msg: Message):
# #     await msg.answer(f"Твой ID: {msg.from_user.id}")

# @dp.message(lambda message: message.text in ['Профиль', 'Партнерская программа', 'Банк', 'Ресурсы'])
# async def menu_handler(message: types.Message):
#     await message.answer(f"Ты выбрал раздел {message.text}")