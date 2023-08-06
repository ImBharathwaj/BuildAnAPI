import time
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

app = FastAPI()


# Creating a schema for the post which is going to be passed into the API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host="localhost", dbname="fastapi", user="postgres", password="root"
        )
        cursor = conn.cursor()
        print("Database connected succefully!")
        break
    except Exception as err:
        print(f"Error occurred while connecting database!")
        print(f"Error: {err}")
        time.sleep(2)

my_post = [
    {
        "title": "I am the great",
        "content": "MLK is a great person",
        "published": True,
        "rating": -10,
        "id": 1,
    },
    {
        "title": "I am the great",
        "content": "Mike is a great person",
        "published": True,
        "rating": -10,
        "id": 2,
    },
    {
        "title": "I am the great",
        "content": "Ali is a great person",
        "published": True,
        "rating": -10,
        "id": 3,
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
    query_str = f"""INSERT INTO posts(title, content, published) VALUES('{post.title}', '{post.content}', '{post.published}') RETURNING *;"""
    cursor.execute(query=query_str)
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}


# Getting all post out from posts table
@app.get("/posts")
def posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post) - 1]
    return {"post": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    query_str = f"""SELECT * FROM posts WHERE id = {id}"""
    cursor.execute(query=query_str)
    post = cursor.fetchone()
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
    query_str = f"""DELETE FROM posts WHERE id = {id} RETURNING *"""
    cursor.execute(query=query_str)
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    query_str = f"""UPDATE posts SET title='{post.title}', content='{post.content}', published='{post.published}' WHERE id = {id} RETURNING *"""
    cursor.execute(query=query_str)
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    return {"data": "Updated successfully"}
