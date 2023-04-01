from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pw import _password, _user, _db, _host
from enum import Enum

class Sort_by(str, Enum):
    ID = 'ID'
    TITLE = 'Title'
    PUBLISHED = 'Published'
    CREATED = 'Created'

class Sort_type(str, Enum):
    ASCENDING = 'Ascending'
    DESCENDING = 'Descending'

class Sort_bool(str, Enum):
    TRUE = 'True'
    FALSE = 'False'

while(True):
    try:
        conn = psycopg2.connect(host=_host, database=_db, user=_user, 
                                password=_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection succesful")
        break
    except Exception as error:
        print(f"Connection failed, error: {error}, retrying in 3 seg")
        time.sleep(3)

app = FastAPI(title="API with Postgress DB", version="0.1", 
              contact={
                    "name": "My github",
                     "url": "https://github.com/chavezmg"})

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get('/')
async def root():
    return {"Welcome": "to my API"}

@app.get('/sort')
async def sort(sort_by: Sort_by, sort_type: Sort_type, sort_bool: Sort_bool):
    print(sort_by.value)
    if(sort_by.value=='ID'):
        if(sort_type.value=='Ascending'):
            cursor.execute("""SELECT * FROM posts ORDER BY id ASC """)
            post = cursor.fetchall()
        else:
            cursor.execute("""SELECT * FROM posts ORDER BY id DESC """)
            post = cursor.fetchall()
    elif(sort_by.value=='Title'):
        cursor.execute("""SELECT * FROM posts ORDER BY title ASC """)
        post = cursor.fetchall()
        if(sort_type.value=='Ascending'):
            cursor.execute("""SELECT * FROM posts ORDER BY title ASC """)
            post = cursor.fetchall()
        else:
            cursor.execute("""SELECT * FROM posts ORDER BY title DESC """)
            post = cursor.fetchall()
    elif(sort_by.value=='Published'):
        if(sort_bool=='True'):
            cursor.execute("""SELECT * FROM posts WHERE published=true""")
            post = cursor.fetchall()
        else:
            cursor.execute("""SELECT * FROM posts WHERE published=false""")
            post = cursor.fetchall()
    elif(sort_by.value=='Created'):
        if(sort_type.value=='Ascending'):
            cursor.execute("""SELECT * FROM posts ORDER BY created_at ASC""")
            post = cursor.fetchall()
        else:
            cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC """)
            post = cursor.fetchall()

    return {'Sorted data': post}


@app.get('/posts')
async def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}

@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if (post != None):
        return {'data': post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f'Post with id: {id} not found')

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) 
                    VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {'data': new_post}

@app.delete('/posts/{id}')
async def delete_post(id: int):    
    cursor.execute(f""" DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = cursor.fetchone()
    if (post!=None):
        conn.commit()
        return {'data': post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f'Post with id: {id} not found')

@app.put('/posts/{id}'  )
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                    (post.title, post.content, post.published, id))
    post_updated = cursor.fetchone()
    if (post_updated != None):
        conn.commit()
        return {'data': post_updated}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f'Post with id: {id} not found')



