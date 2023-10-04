from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Currencies(Base):
    __tablename__ = "currencies"

    id: Mapped[int]  = mapped_column( primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)


class SubCurrencies(Base):
    __tablename__ = "sub_currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cur_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))


class Addresses(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    address: Mapped[str] = mapped_column(unique=True)



class Statistic(Base):
    __tablename__ = "statistic"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,autoincrement=True)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id"))
    sub_currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("sub_currencies.id"))
    balance: Mapped[float]
    updated_at: Mapped[datetime]
