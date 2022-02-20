from random import randrange
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, validator

import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):  # Post class extends BaseModel
    title: str
    content: str
    published: bool = True  # if user doesn't provide published value, use 'True' as default
    rating: Optional[int] = None # if user doesn't provide value, defaults to None

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_db', user='root', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connection to db failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "Post 1 Title", "content": "Post1 Content", "id": 123},
{"title": "Post 2 Title", "content": "Post2 Content", "id": 234}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# below routes are PATH OPERATIONS


@app.get("/")  # decorator that passes REST method to endpoint, connects to app
async def root():  # function that implements route
    return {"message": "Hello World 123"}


@app.get("/posts/")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):  # stores post req data in new_post var, validates against Post schema
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone() 
    conn.commit()  # saves changes to postgres db
    
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):  # ensure id from params is retrieved as integer
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    print(updated_post)
    
    return {"data": updated_post}