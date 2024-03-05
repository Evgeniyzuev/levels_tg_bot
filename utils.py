import random
import logging
import db


def bonus_open():
        bonus = 0
        bonus += random.randint(0, 159)
        bonus = bonus ** 3
        bonus = bonus / 1000
        bonus = bonus + 1003
        bonus = round(bonus)
        db.bonus_size = int (bonus)
        db.real_estate += int (bonus)
        db.bonuses_available -= 1
    

def get_balance():
    return (db.real_estate + db.grow_wallet + db.liquid_wallet)
