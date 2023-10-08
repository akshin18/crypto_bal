from sqlalchemy.orm import Session
from datetime import datetime

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
        db.refresh(db_item)
    except Exception as e:
        db.rollback()


def get_wallets(sub, db: Session):
    data = db.query(models.Statistic).filter_by(sub_currency_id=sub).all()
    return data


def check_and_update_balances(db_sql):
    for db in db_sql:
        data = db.query(models.Addresses).all()
        print(data[0])
        print(data[0].statistic)