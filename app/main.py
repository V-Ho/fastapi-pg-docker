from random import randrange
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, validator


app = FastAPI()

class Post(BaseModel):  # Post class extends BaseModel
    title: str
    content: str
    published: bool = True  # if user doesn't provide published value, use 'True' as default
    rating: Optional[int] = None # if user doesn't provide value, defaults to None


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
def get_posts():
    return {"data": my_posts}


@app.post("/create_posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):  # stores post req data in new_post var, validates against Post schema
    new_post_dict = new_post.dict() # converts response new_post into dict
    new_post_dict['id'] = randrange(0, 1000000) # assigns post an id
    my_posts.append(new_post_dict)
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):  # ensure id from params is retrieved as integer
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index in array that has post id
    # remove from index with array.pop
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}