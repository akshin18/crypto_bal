from sqlalchemy.orm import Session

from . import models, schemas


def get_currencies(db: Session):
    currencies = db.query(models.Currencies).all()

    for currency in currencies:
        sub_currencies=  [x.name for x in db.query(models.SubCurrencies).filter_by(cur_id=currency.id).all()]
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