from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#Board
class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List, Optional

# --- Column ---
class ColumnBase(BaseModel):
    name: str
    order: Optional[int] = 0

class ColumnCreate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int
    board_id: int

    class Config:
        orm_mode = True

# --- Card ---
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    column_id: int

    class Config:
        orm_mode = True