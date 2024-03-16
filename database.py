import asyncio
from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship




Base = declarative_base()

# Association table for the many-to-many relationship between users and referrers
user_referrer = Table('user_referrer', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('referrer_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    referral_link = Column(String, unique=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.user_id"))
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
engine = create_engine("sqlite:///bot.db")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


































users = {}