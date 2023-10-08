from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Currencies(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)


class SubCurrencies(Base):
    __tablename__ = "sub_currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cur_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    name: Mapped[str]


class Addresses(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(unique=True)

    statistic: Mapped[list["Statistic"]] = relationship(back_populates="address",cascade="all, delete-orphan", uselist=True)


class Statistic(Base):
    __tablename__ = "statistic"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id", ondelete="CASCADE"))
    sub_currency_id: Mapped[int] = mapped_column(ForeignKey("sub_currencies.id"))
    balance: Mapped[float]
    native_balance: Mapped[float | None] = mapped_column(default=0.0)

    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now)

    address: Mapped["Addresses"] = relationship(back_populates="statistic")
