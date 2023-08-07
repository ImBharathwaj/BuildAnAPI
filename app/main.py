import time
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session

# Creating an instance for application with FastAPI class
app = FastAPI()

# Binding database with engine and
models.Base.metadata.create_all(bind=engine)


# Creating a schema for the post which is going to be passed into the API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/")
def read_root():
    return {"key": "value"}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def createpost(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    return {"post": post.model_dump()}


@app.get("/posts")
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Data": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print("From get one method: ", post)
    print(type(post))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exists",
        )
    # print(type(post))
    # post.update(, synchronize_session=False)

    db.commit()
    return {"data": post}
