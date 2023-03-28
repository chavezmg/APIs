from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

posts_db = [{"id": 0, "title": "titulo post1", "contenido": "contenido post 1"}, 
{"id":1, 'title': "comidas favoritas", 'contenido': "pizza"}]

@app.get('/')
async def root():
    return {"f root": "Cuerpo f root"}

@app.get('/posts')
async def get_posts():
    return {"data": posts_db}

@app.get("/posts/{id}")
async def get_post(id: int):
    for post in posts_db:
        if post['id'] == int(id):
            return {"post_detail": post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} not found")

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 9999999999)
    posts_db.append(post_dict)
    return {"data": post_dict} 

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    for index, post in enumerate(posts_db):
        if post['id'] == int(id):
            posts_db.pop(index)
            return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} not found")

@app.put("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: Post):
    for index, ipost in enumerate(posts_db):
        if ipost['id'] == int(id):
            posts_db[index] = post.dict()
            posts_db[index]['id'] = id
            return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id: {id} not found")