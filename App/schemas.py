

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailError, EmailStr, conint

class post(BaseModel):
    title: str
    content:str
    published:bool=True
    rating:Optional[int]=None

class createpost(post):
    pass

class userout(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True

class response(post):
    id:int
    created_at:datetime
    user_id:int
    user:userout
    class Config:
        orm_mode = True

class get_vote(BaseModel):
    Post:response
    votes:int
    class Config:
        orm_mode = True


class createuser(BaseModel):
    email:EmailStr
    password:str


class login(BaseModel):
    email:EmailStr
    password:str

class token(BaseModel):
    access_token:str
    token_type:str

class Tokendata(BaseModel):
    id:Optional[str]=None

class vote(BaseModel):
    post_id:int
    dir:conint(le=1)
