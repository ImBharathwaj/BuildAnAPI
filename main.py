from random import randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


# Creating a schema for the post which is going to be passed into the API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = []


@app.get("/")
def read_root():
    return {"key": "value"}


@app.get("/posts")
def works():
    return {"data": my_post}


def find_post(id):
    for i in my_post:
        # print(id)
        if i["id"] == id:
            return i
        return {"Data": "Not found"}


@app.get("/posts/{id}")
def get_post(id):
    post = find_post(str(id))
    print(post)
    print(type(post))
    return {"post_detail": post}


@app.post("/createpost")
# payLoad: dict = Body(...)
# ^ Basic method to get data out of the body without using any framework
def createpost(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = str(randrange(0, 100000000))
    my_post.append(post_dict)
    return {"post": my_post}
