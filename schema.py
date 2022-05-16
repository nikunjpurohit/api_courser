from pydantic import BaseModel, EmailStr
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from datetime import datetime
from typing import Optional

from pydantic.types import conint
from sqlalchemy import Integer


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email: EmailStr

    class Config:
        orm_mode = True