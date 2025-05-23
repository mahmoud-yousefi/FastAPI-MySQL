from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    
class CommentBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    db.delete(db_post)
    db.commit()
    
@app.post("/comments/", status_code=status.HTTP_201_CREATED)
async def create_post(comment: CommentBase, db: db_dependency):
    db_post = models.Comment(**comment.model_dump())
    db.add(db_post)
    db.commit()
    
@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def read_post(comment_id: int, db: db_dependency):
    post = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Comment not found')
    return post

@app.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def read_post(comment_id: int, db: db_dependency):
    db_post = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Comment not found')
    db.delete(db_post)
    db.commit()    

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    try:
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        print(**user.model_dump()) # this line cause error
        return {"message": "User created successfully "}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"Error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user