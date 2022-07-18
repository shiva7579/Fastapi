from .. import schemas
from .. import password
from .. import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,status,Depends,APIRouter,Response
from ..Database import get_db
from typing import List, Optional
from .. import oauth2
from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=['posts'])

#@router.get("/",response_model=List[schemas.response])
@router.get("/",response_model=List[schemas.get_vote])
def multi(db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #print(posts)
    #return {"Data":posts}
    #Success= db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
    #Success= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    Success= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return Success

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.response)
def first(phrase:schemas.createpost ,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(phrase.title,phrase.content)) 
    #new_post=cursor.fetchone()
    #conn.commit()
    #return {"Did it":new_post}
    #sqlalchemy
    #new_post=models.Post(title=phrase.title,content=phrase.content,published=phrase.published)
    #Instead of adding all columns we use **phrase.dict
    print(current_user.email)
    new_post=models.Post(user_id=current_user.id,**phrase.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=schemas.response)
def get_posts(id:int,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),)) 
    #select_post=cursor.fetchone()
    get_post= db.query(models.Post).filter(models.Post.id==id)
    get=get_post.first()
    if not get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id '{id}' is not found")
       # response.status_code=status.HTTP_404_NOT_FOUND
        #return{'Message': f"Id '{id}' is not found"} 
    #if get.user_id !=current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized")

    return get


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),)) 
    #delete_post=cursor.fetchone()
    #conn.commit()
    delete_post=db.query(models.Post).filter(models.Post.id==id)
    delete=delete_post.first()
    if delete== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id '{id}' is not found")
    if delete.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.response)
def update_post(id:int,phrase:schemas.createpost,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s,content=%s,rating=%s WHERE id=%s RETURNING *""",(phrase.title,phrase.content,phrase.rating,str(id),))
    #update_post=cursor.fetchone()
    #conn.commit()
    update_post=db.query(models.Post).filter(models.Post.id==id)
    update=update_post.first()

    if update== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id '{id}' is not found")
    if update.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized")
    update_post.update(phrase.dict(),synchronize_session=False)
    db.commit()
    return update
