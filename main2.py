from http.client import HTTPException
from multiprocessing.sharedctypes import synchronized
from urllib import response
from typing import List
from certifi import contents
from fastapi import FastAPI, status, Response
from numpy import deprecate
from pydantic import BaseModel
from passlib.context import CryptContext
from random import randrange
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from requests import Response
import time
import schema
from sqlalchemy import Boolean
import utils
import models
from databse import engine,SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
app = FastAPI()


models.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
    


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/sqlaclhemy')
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data":post}

my_posts=[{"title":"tiitle of post 1","content":"conentnt of posts 1","id":1},{"title":"favorite food","content":"I like pizza","id":2}]

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None





@app.post("/items")
def create_item(item: Item):
    print(item.name)
    return (item.name) 


@app.post("/tosts")
def posts(post: schema.PostBase, db: Session = Depends(get_db)):
    #my_posts=models.Post(title=post.title,content=post.content, published = post.published )
    my_posts=models.Post(**post.dict() )
    db.add(my_posts)
    db.add(my_posts)
    db.commit()
    db.refresh(my_posts)
    
    return {"data": my_posts}



@app.post("/posts")
def posts_append(post: Item):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}



def find_post(id):
    for p in my_posts:
        if int(p["id"]) == int(id):
            return p
        

@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    new_post =db.query(models.Post).filter(models.Post.id==id).first()
    print(new_post)
    if not new_post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message':f'post with id {id} was not found'}

    return{"post_detail": new_post}


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if int(p['id'])==int(id):
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    #deleting posts
    #find the index in the array that has required id
    #my_posts.pop(index)
    del_post = db.query(models.Post).filter(models.Post.id==id)
    print(del_post)
    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} doesnt exists')

    
    del_post.delete(synchronize_session=False)
    db.commit()
    #return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,post: Item):
    index =find_index_post(id)
    print(index)

    if index ==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")

    post_dict =post.dict()
    post_dict['id']=id
    my_posts[index] = post_dict
    return{'data': post_dict}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hash_password = utils.hash(user.password)
    user.password=hash_password
    new_user=  models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',response_model=schema.UserOut)
def get_user(id:int,  db: Session = Depends(get_db)):
    
    user_data = db.query(models.User).filter(models.User.id==id).first()
    print(id)
    if not user_data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")

    return user_data