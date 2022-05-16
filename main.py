from http.client import HTTPException
from urllib import response
from fastapi import FastAPI, status, Response
from pydantic import BaseModel
from random import randrange
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from requests import Response
import time
app = FastAPI()


while True:
    try:
        conn =psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
        cursor =conn.cursor()
        print("databse Connection was succesful")
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        
        break
    except Exception as error:
        print("connecting to database failed")
        print("EWrror:",error)
        time.sleep(2)

    


@app.get("/")
def read_root():
    return {"Hello": "World"}


my_posts=[{"title":"tiitle of post 1","content":"conentnt of posts 1","id":1},{"title":"favorite food","content":"I like pizza","id":2}]

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None




@app.post("/items")
def create_item(item: Item):
    cursor.execute("""INSERT INTO posts (name, description,price, tax) VALUES (%s,%s,%s,%s) RETURNING *""",(item.name, item.description, item.price, item.tax))
    new_post = cursor.fetchall()
    conn.commit()
    print(new_post)
    return (new_post) 


@app.get("/posts")
def posts():
    posts = cursor.execute("""SELECT * FROM posts""")
    posts= cursor.fetchall()
    print(posts)
    return {"data": posts}



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
def get_posts(id):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id))
    test_posts =cursor.fetchall()
    print(test_posts)
    if not test_posts:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message':f'post with id {id} was not found'}

    return{"post_detail": test_posts}


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if int(p['id'])==int(id):
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting posts
    #find the index in the array that has required id
    #my_posts.pop(index)
    index = find_index_post(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} doesnt exists')

    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

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