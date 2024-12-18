from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TopUpRequest(BaseModel):
    amount: float

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_username: str
    amount: float
    description: Optional[str] = None

    class Config:
        orm_mode = True  # Включаем поддержку ORM для корректного преобразования

class TransactionOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    description: Optional[str]
    date: datetime

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    bonus_level: int
    balance: float
    transactions: List[TransactionOut]

    class Config:
        orm_mode = True
