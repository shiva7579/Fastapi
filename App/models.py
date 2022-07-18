from time import timezone
from xmlrpc.client import Boolean

from pydantic import EmailStr
from .Database import Base
from sqlalchemy import  TIMESTAMP, Column, ForeignKey,String,Integer,Boolean, text
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__="posts"
    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True')
    rating=Column(Integer,server_default='5')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')) 
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    user=relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,nullable=False,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__="vote"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)