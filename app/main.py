from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


# Creating a schema for the post which is going to be passed into the API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [
    {
        "title": "I am the great",
        "content": "MLK is a great person",
        "published": True,
        "rating": -10,
        "id": 1
    },
    {
        "title": "I am the great",
        "content": "Mike is a great person",
        "published": True,
        "rating": -10,
        "id": 2
    },
    {
        "title": "I am the great",
        "content": "Ali is a great person",
        "published": True,
        "rating": -10,
        "id": 3
    },
]


def find_post(id: int):
    for p in my_post:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


@app.get("/")
def read_root():
    return {"key": "value"}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
# payLoad: dict = Body(...)
# ^ Basic method to get data out of the body without using any framework
def createpost(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000)
    my_post.append(post_dict)
    return {"post": my_post}


@app.get("/posts")
def posts():
    return {"data": my_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post) - 1]
    return {"post": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with {id} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )
    return {"post_detail": post}


# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Find an index of the post for the respective id in the list
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    # Find an index of the post for the respective id in the list
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data": "Updated successfully"}
