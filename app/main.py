from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine) # automatically creates tables from models.py in postgres


app = FastAPI()


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


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # PGQUERY
    # cursor.execute("""SELECT * FROM pg_posts """)
    # posts = cursor.fetchall()

    # SQLALCHEMY
    # stores req as variable 'db'
    # get_db: creates session for every api req
    # each req queries method on Post model, which connects to posts pg table
    
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 

    new_post = models.Post(**post.dict()) # automatically includes all Model fields
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)): 
    # cursor.execute("""SELECT * FROM pg_posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM pg_posts where id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE pg_posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
