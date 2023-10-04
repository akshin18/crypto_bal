from pydantic import BaseModel, validator
from datetime import datetime
from db import models

class CreateCurrency(BaseModel):
    name: str


class CreateSubCurrency(BaseModel):
    name: str
    cur_id: int


class GetCurrency(BaseModel):
    name: str
    sub_currencies: list

    class Config:
        from_attributes = True


class Currency(GetCurrency):
    id: int


class SubCurrency(BaseModel):
    id: int
    name: str
    cur_id: int

    class Config:
        from_attributes = True


class Address(BaseModel):
    address: str
    balance: float | None


class Statistics(BaseModel):
    id: int
    balance: int
    updated_at: datetime
    address: Address

    @validator('address')
    def inject_id(cls, v):
        v.balance = v.balance if v.balance != None else 0
        return v
