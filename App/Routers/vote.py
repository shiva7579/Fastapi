from .. import schemas
from .. import password
from .. import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,status,Depends,APIRouter,Response
from ..Database import get_db
from typing import List, Optional
from .. import oauth2

router=APIRouter(prefix="/vote",tags=['votes'])
@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.vote,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):

    posts=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} doesnot exist")
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You have already voted this post")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        # new_vote=models.Vote(**vote.dict()) error:TypeError: 'dir' is an invalid keyword argument for Vote
        db.add(new_vote)
        db.commit()
        return{"message":"You successfully voted the post"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You never voted this post")
        vote_query.delete(synchronize_session=False)
        return{"message":"you vote is successfully deleted"}



       
         