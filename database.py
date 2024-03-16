import asyncio
from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, FLOAT,DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

Base = declarative_base()


# Association table for the many-to-many relationship between users and referrers
user_referrer = Table('user_referrer', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('referrer_id', Integer, ForeignKey('users.user_id'), primary_key=True))


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    referral_link = Column(String, unique=True)
    referrer_id = Column(Integer, ForeignKey("users.user_id"))
    registration_time = Column(DATETIME)
    level = Column(Integer, index=True)
    real_estate = Column(FLOAT)
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
    bonus_cd_time = Column ( String)
    # referrer = relationship("User", back_populates="referred")
    # referrals = relationship("User", 
    #                         secondary=user_referrer, 
    #                         primaryjoin=id==user_referrer.c.user_id, 
    #                         secondaryjoin=id==user_referrer.c.referrer_id,
    #                         backref="referrers")

    # referrer = relationship("User", back_populates="referred")
    # referred = relationship("User", back_populates="referrer")
    # subscribers = relationship("User", back_populates="subscriber")
    # subscriber = relationship("User", back_populates="referrals")

# DATABASE_URL = "sqlite:///bot.db"

#  database.users[user_id] = {"referrers": [referrer_id], "referrals": [], "referral_link": referral_link, "bonus_cd": time_now}


engine = create_engine("sqlite:///bot.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_or_create_user(db, user_id, user_name, referral_link, referrer_id):   # user = await db.query(User).filter(User.id == user_id).first()
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        now = datetime.now()
        # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        # time_now_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        referrers_text = f'{referrer_id}'
        user = User(user_id=user_id, user_name=user_name, referral_link=referral_link, referrer_id=referrer_id, registration_time=now, level=0,
            real_estate=0, grow_wallet=0, liquid_wallet=0, turnover=0, sales=0, bonuses_available=0, bonuses_gotten=0, guide_stage=0,
            current_leader_id=referrer_id, referrers=referrers_text, referrals = '', bonus_cd_time = now 
                  )
        db.add(user)
        db.commit()
        # if referrer_id:
        #     # referrer = await db.query(User).filter(User.id == referrer_id).first()
        #     referrer = db.query(User).filter(User.user_id == referrer_id).first()
        #     if referrer:
        #         user.referrer_id = referrer.user_id
        #         referrer.subscribers.append(user)
    return user 

async def get_user(db, user_id):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user  

async def user_info(db, user_id):
    user = db.query(User).filter(User.user_id == user_id).first()
    user_info = (f"Registration Successful\nuser_id: {user.user_id}\nuser_name: {user.user_name}\nreferral_link:\n{user.referral_link}\nreferrer_id: {user.referrer_id}\nregistration_time:\n{user.registration_time}" 
    + f"\nlevel: {user.level}\nreal_estate: {user.real_estate}\ngrow_wallet: {user.grow_wallet}\nliquid_wallet: {user.liquid_wallet}\nturnover: {user.turnover}\nsales: {user.sales}\
    \nbonuses_available: {user.bonuses_available}\nbonuses_gotten: {user.bonuses_gotten}\nguide_stage: {user.guide_stage}\ncurrent_leader_id: {user.current_leader_id}\nreferrers: {user.referrers}"
    + f'\nbonus_cd_time:\n{user.bonus_cd_time}')
    return user_info
#+f'{user.registration_time}'




























users = {}