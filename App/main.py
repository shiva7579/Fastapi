
from random import randrange
from typing import List
from fastapi import FastAPI


#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from . import models
from .Database import  engine
from .Routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware 
#after using alembic we dont need below code
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#while True:
        #try:
            #conn=psycopg2.connect(host='localhost',database='APP',user='postgres',password='fastapi',cursor_factory=RealDictCursor)
            #cursor=conn.cursor()
            #print("Database is connected successfully")
            #break
        #except Exception as error:
            #print("connecting to server failed")
            #print("Error:",error)
            #time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


memory=[{"Title":"My first post!!","id":1}]
def find_post(id):
    for p in memory:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i,p in enumerate(memory):
        if p["id"]==id:
           return i
          




#User Registration

