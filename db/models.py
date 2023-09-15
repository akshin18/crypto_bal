from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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


