from typing import List
from pydantic import BaseModel


class CreateCurrency(BaseModel):
    name: str


class CreateSubCurrency(BaseModel):
    name: str
    cur_id: int


class GetCurrency(BaseModel):
    name: str
    sub_currencies: list


    class Config:
        orm_mode = True

class Currency(GetCurrency):
    id: int
    

class SubCurrency(BaseModel):
    id: int
    name: str
    cur_id: int

    class Config:
        orm_mode = True

    