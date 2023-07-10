from typing import Optional
from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import SystemRandom


system_random = SystemRandom()
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "favourite food",
        "content": "i like pizza",
        "id": 2,
    }
]


def find_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index, post

    return None, None

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    _, post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} was not found"
        )

    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = system_random.randrange(0, 10000000)
    my_posts.append(post_dict)
    return {
        "data": post_dict
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index, _ = find_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} was not found"
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index, _ = find_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} was not found"
        )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
