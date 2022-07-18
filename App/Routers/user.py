from .. import schemas
from .. import password
from .. import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,status,Depends,APIRouter
from ..Database import get_db

router=APIRouter(prefix="/users",tags=['users'])
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.userout)
def users(users:schemas.createuser,db: Session = Depends(get_db)):
    hashed_password=password.hash(users.password)
    users.password=hashed_password
    if db.query(models.User).filter(models.User.email==users.email).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Email already exist")

    new_user=models.User(** users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.userout)
def get_user(id:int,db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id '{id}' is not found")
    return user