
from fastapi import APIRouter, FastAPI,Response,status,Depends,HTTPException
from .. import schemas
from .. import Database,models,password,oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.token)
#def login(user_credential:schemas.login,db: Session = Depends(Database.get_db)):
    #user=db.query(models.User).filter(models.User.email==user_credential.email).first()

def login(user_credential:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(Database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    if not password.verify_login(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    access_token=oauth2.create_access_token ( data={"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}


