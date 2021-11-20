import pydantic as _pydantic
from sqlalchemy.sql.expression import true
from pydantic import BaseModel


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class _PaymentMethodBase(_pydantic.BaseModel):
    payment_type: str
    name: str


class PaymentMethodCreate(_PaymentMethodBase):
    pass


class PaymentMethod(_PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True


class _PaymentBase(_pydantic.BaseModel):
    packet: str
    payment_method: str
    price: int


class PaymentCreate(_PaymentBase):
    pass


class Payment(_PaymentBase):
    id: int

    class Config:
        orm_mode = True
