from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field
import time
from typing import Optional, List 
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token, validate_token

app = FastAPI()

app.title = "Mi primer aplicacion de Peliculas"
app.version = "0.0.1"

class User(BaseModel):
    email: str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=2,max_length=40)
    overview:str = Field(min_length=20,max_length=300)
    year:int = Field(le=time.localtime().tm_year)
    rating:float = Field(ge= 0, le=10)
    category:str = Field(min_length=5,max_length=12)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

@app.get("/",tags=['home'])
def message():
    return HTMLResponse(content = "<h1>Hola Mundo!!!!</h1>")

@app.get("/movies",tags=['movies'],response_model= List[Movie],status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)



@app.get("/movies/id/{id}",tags=['movies'],response_model= Movie,status_code=200)
def get_movies(id:int = Path(ge=1,le=2000)):
    movie = list(filter(lambda movie: movie['id'] == id, movies))
    if len(movie) > 0:
        response = JSONResponse(status_code=200,content=movie)
    else:
        response = JSONResponse(status_code=404,content={"message":"Movie not found"})
    return response

@app.get("/movies/",tags=['movies'],response_model=List[Movie])
def get_category(category:str = Query(min_length=5,max_length=12)):
    movie = [movie for movie in movies if movie['category'] == category]
    if len(movie) > 0:
        response = JSONResponse(status_code=200,content=movie)
    else:
        response = JSONResponse(content={"message":"Category not found"},status_code=404)
    return response

""" @app.post("/movies",tags=['movies'])
def create_movie(movie:dict):
    movies.append(movie)
    return movies """

""" @app.post("/movies",tags=['movies'])
def create_movie(id:int,
                    title:str,
                    overview:str,
                    year:str,
                    rating:float,
                    category:str):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies """
@app.post("/movies",tags=['movies'], status_code=201)
def create_movie(movie:Movie):
    movies.append(movie)
    return JSONResponse(content={"message":"Movie created successfully"}, status_code=201)

""" @app.put("/movies/{id}",tags=['movies'])
def update_movie(id:int,
                    title:str = Body(),
                    overview:str = Body(),
                    year:str = Body(),
                    rating:float = Body(),
                    category:str = Body() ):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
    return movies """

@app.put("/movies/{id}",tags=['movies'])
def update_movie(movie : Movie):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
    return JSONResponse(content={"message":"Movie updated successfully"}, status_code=200)


""" @app.delete("/movies/{id}",tags=['movies'])
def delete_movie(id:int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies """
@app.delete("/movies/{id}",tags=['movies'], response_model=dict) #Response_model es para que no se muestre el contenido de la lista
def delete_movie(id:int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return JSONResponse(content={"message":"Movie deleted successfully"}, status_code=200)

@app.post("/login",tags=['auth'], response_model=dict,status_code=200)
def login(user:User):
    if user.email == "admin@mail.com" and user.password == "1234567890":
        token = create_token(data={"user":user.model_dump()})
        result = JSONResponse(content ={"token":token},status_code=200)
    else:
        result = JSONResponse(content={"message":"Invalid credentials"},status_code=401)
    return result