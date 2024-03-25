import asyncio
import database
from misc import dp, bot
from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, FLOAT,DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import select, update
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta




engine = create_engine("sqlite:///data/bot.db")
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Association table for the many-to-many relationship between users and referrers
# user_referrer = Table('user_referrer', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
#     Column('referrer_id', Integer, ForeignKey('users.user_id'), primary_key=True))


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    referral_link = Column(String, unique=True)
    referrer_id = Column(Integer, ForeignKey("users.user_id"))
    registration_time = Column(DateTime)
    level = Column(Integer, index=True)
    restate = Column(FLOAT)
    grow_wallet = Column(FLOAT)
    liquid_wallet = Column(FLOAT)
    turnover = Column(FLOAT)
    sales = Column(Integer)
    bonuses_available = Column(Integer)
    bonuses_gotten = Column(Integer)
    guide_stage = Column(Integer)
    current_leader_id = Column(Integer, index=True)
    referrers = Column(String)
    referrals = Column(String)
    bonus_cd_time = Column ( DateTime)

Base.metadata.create_all(bind=engine)

# db = SQLAlchemy(app)
# database.db = database.SessionLocal()

async def get_or_create_user(user_id, user_name, referral_link, referrer_id,):   # user = await db.query(User).filter(User.id == user_id).first()

    with Session(expire_on_commit=False) as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        # await bot.send_message(user_id, "пользователь загружен")
        session.close()
    if not user:
        with Session(expire_on_commit=False) as session:
            # await bot.send_message(user_id, "регистрация нового пользователя")
            now = datetime.now()
            referrers_text = ''
            referrers_text += f'{referrer_id}'
            if user_id == 6251757715: level = 100
            else: level = 0
            user = User(user_id=user_id, user_name=user_name, referral_link=referral_link, referrer_id=referrer_id, registration_time=now, level=level,
                restate=0, grow_wallet=0, liquid_wallet=0, turnover=0, sales=0, bonuses_available=0, bonuses_gotten=0, guide_stage=0,
                current_leader_id=referrer_id, referrers=referrers_text, referrals = '', bonus_cd_time = now 
                    )
            session.add(user)
            session.commit()

        # db.close()
        # if referrer_id:
        #     # referrer = await db.query(User).filter(User.id == referrer_id).first()
        #     referrer = db.query(User).filter(User.user_id == referrer_id).first()
        #     if referrer:
        #         user.referrer_id = referrer.user_id
        #         referrer.subscribers.append(user)
    # await bot.send_message(user_id, f"Добавлен {user.user_name}\n с балансом {user.restate}")
    try: 
        current_leader = await database.get_user(referrer_id)
        # text = (referrer_id +': ' + current_leader.user_name + 'lvl: ' + current_leader.level + '\n')
        # user.referrers += text 
    except: 
        text = f'Ваш лид: {referrer_id} не найден в базе'
        await bot.send_message(user_id, text)
    # database.local_users[user_id] = user
    # local_user = database.local_users[user_id]
    # await bot.send_message(user_id, f"Добавлен {user.user_name}\nс балансом {user.restate}")  
    return user 

async def get_user(user_id):
    # try:
    #     local_users[user_id] = database.local_users[user_id]
    #     # await bot.send_message(user_id,"get_user: Пользователь найден")
    #     return  local_users[user_id]
    # except:
    #     try:
            with Session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
            # database.local_users[user_id] = user
            return user
        # except:
        #     await bot.send_message(user_id, 'user not found') 
    # else:
            
#  
async def user_info(user_id):

    user = await get_user(user_id)
    registration_time = user.registration_time.strftime('%Y-%m-%d %H:%M:%S')   # [user_id]
    bonus_cd_time = user.bonus_cd_time.strftime('%Y-%m-%d %H:%M:%S') # [user_id]
    user_info = (f"\nuser_id: {user.user_id}\nuser_name: {user.user_name}\nreferral_link:\n{user.referral_link}\nreferrer_id: {user.referrer_id}\nregistration_time:\n{registration_time}" 
    + f"\nlevel: {user.level}\nrestate: {user.restate}\ngrow_wallet: {user.grow_wallet}\nliquid_wallet: {user.liquid_wallet}\nturnover: {user.turnover}\nsales: {user.sales}\
    \nbonuses_available: {user.bonuses_available}\nbonuses_gotten: {user.bonuses_gotten}\nguide_stage: {user.guide_stage}\ncurrent_leader_id: {user.current_leader_id}\nreferrers: {user.referrers}"
    + f'\nbonus_cd_time:\n{bonus_cd_time}')
    return user_info
    # except:
    #     await bot.send_message(user_id, "Бот не обновляется♻️\nПерезайдите по реф.ссылке или попробуйте позднее") 
   


# local_users = {}
ubicoin = 250
gamma = {}
payment_to_check = {}
payment_to_check_user_id = 0
payment_to_check_amount = 0
# users = {}