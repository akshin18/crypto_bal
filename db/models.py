from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Currencies(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, unique=True, index=True)


class SubCurrencies(Base):
    __tablename__ = "sub_currencies"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    cur_id = Column(Integer, ForeignKey("currencies.id"))


class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    address = Column(String,unique=True ,sqlite_on_conflict_unique='CASCADE',index=True)



class Statistic(Base):
    __tablename__ = "statistic"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    sub_currency_id = Column(Integer, ForeignKey("sub_currencies.id"))
    balance = Column(Double)
    updated_at = Column(DateTime)

    # __table_args__ = (
    #     UniqueConstraint('address_id', 'sub_currency_id', name='uq_address_sub_currency'),
    # )
