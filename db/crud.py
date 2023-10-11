from sqlalchemy.orm import Session
from datetime import datetime
import copy

from checker.checker import Checker

from . import models, schemas,database


def get_currencies(db: Session):
    currencies = db.query(models.Currencies).all()

    for currency in currencies:
        sub_currencies=  [{"name":x.name,"id":x.id} for x in db.query(models.SubCurrencies).filter_by(cur_id=currency.id).all()]
        currency.sub_currencies = sub_currencies

    return currencies


def get_sub_currencies(db: Session):
    currencies=  db.query(models.SubCurrencies).all()
    grouped_currencies = {}
    for currency in currencies:
        cur_id = currency.cur_id
        name = currency.name
        if cur_id not in grouped_currencies:
            grouped_currencies[cur_id] = []
        grouped_currencies[cur_id].append(name)
    
    # Convert the dictionary values to lists
    grouped_currencies_lists = list(grouped_currencies.values())
    return grouped_currencies_lists


def create_currency(db: Session, currency: schemas.CreateCurrency):
    db_user = models.Currencies(name=currency.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_sub_currency(db: Session, sub_currency: schemas.CreateSubCurrency):
    db_item = models.SubCurrencies(name=sub_currency.name,cur_id=sub_currency.cur_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def add_address_db(db:Session,address: schemas.Address):
    if address.address in [None, ""]: return
    try:
        address_item = models.Addresses(address=address.address)
        db.add(address_item)
        db.commit()
        db.refresh(address_item)

        currencies = [x.id for x in db.query(models.SubCurrencies).all()]
        now = datetime.now()
        for i in currencies:
            db_item = models.Statistic(address_id=address_item.id,sub_currency_id=i,balance=float(0),updated_at=now)
            db.add(db_item)
        db.commit()
        # db.refresh(db_item)
    except Exception as e:
        db.rollback()


def get_wallets(sub, db: Session):
    data = db.query(models.Statistic).filter_by(sub_currency_id=sub).all()
    return data


def check_and_update_balances(db_sql):
    data_dict = {}
    for db in db_sql:
        data = db.query(models.Addresses).all()
        for x in data:
            for zi,i in enumerate(copy.deepcopy(x.statistic)):
                if zi in data_dict:
                    data_dict[zi].append(i)
                else:
                    data_dict.update({zi:[i]})
    distribution_currencies(data_dict)


def distribution_currencies(data_dict: dict):
    checker = Checker()
    checker.check_all()
    for i in data_dict:
        if i == 0:
            #usdt Etherium
            checker.eth_c.add_addresses(1,data_dict[i])
            ...
        elif i == 1:
            #usdc Etherium
            checker.eth_c.add_addresses(2,data_dict[i])
            ...
        elif i == 2:
            #usdc BSC
            checker.bsc_c.add_addresses(2,data_dict[i])
            ...
        elif i == 3:
            #busd BSC
            checker.bsc_c.add_addresses(1,data_dict[i])
            ...
        elif i == 4:
            #usdc Optimism
            checker.opt_c.add_addresses(2,data_dict[i])
            ...
            
        elif i == 5:
            #usdt Optimism
            checker.opt_c.add_addresses(1,data_dict[i])
            ...
            
        elif i == 6:
            #usdt Arbitrum
            checker.arb_c.add_addresses(1,data_dict[i])
            ...
           
        elif i == 7:
            #usdc Arbitrum
            checker.arb_c.add_addresses(2,data_dict[i])
            ...
           
        elif i == 8:
             #tusd Fantom
            checker.fan_c.add_addresses(1,data_dict[i])
            ...
            
        elif i == 9:
            #usdt Avalanche
            checker.ava_c.add_addresses(1,data_dict[i])
            ...
            
        elif i == 10:
            #usdt Polygon
            checker.pol_c.add_addresses(1,data_dict[i])
            ...
           
        elif i == 11:
             #usdc Polygon
            checker.pol_c.add_addresses(2,data_dict[i])
            ...
            
        elif i == 12:
            #usdc Avalanche
            checker.ava_c.add_addresses(2,data_dict[i])
            ...