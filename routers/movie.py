from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieSession
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=2,max_length=40)
    overview:str = Field(min_length=20,max_length=300)
    year:int = Field(le=time.localtime().tm_year)
    rating:float = Field(ge= 0, le=10)
    category:str = Field(min_length=5,max_length=12)


@movie_router.get("/movies",tags=['movies'],response_model= List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)

@movie_router.get("/movies/id/{id}",tags=['movies'],response_model= Movie,status_code=200)
def get_movies(id:int = Path(ge=1,le=2000)):
    db = Session()
    result = db.query(MovideModel).filter(MovideModel.id == id).first()
    response = JSONResponse(content= jsonable_encoder(result),status_code=200)
    if not result:
        response = JSONResponse(content={"message":"Movie not found"},status_code=404)
    return response


@movie_router.get("/movies/",tags=['movies'],response_model=List[Movie])
def get_category(category:str = Query(min_length=5,max_length=12)):
    deb = Session()
    result = db.query(MovideModel).filter(MovideModel.category == category).all()
    response = JSONResponse(content= jsonable_encoder(result),status_code=200)
    if not result:
        response = JSONResponse(content={"message":"Category not found"},status_code=404)
    return response

@movie_router.post("/movies/create",tags=['movies'],response_model=dict, status_code=201)
def create_movie(movie:Movie):
    db = Session()
    new_movie = MovideModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message":"Movie created successfully"}, status_code=201)

@movie_router.put("/movies/{id}",tags=['movies'])
def update_movie(id:int, movie : Movie):
    db = Session()
    result = db.query(MovideModel).filter(MovideModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message":"Movie updated successfully"}, status_code=200)

@movie_router.delete("/movies/{id}",tags=['movies'], response_model=dict)
def delete_movie(id:int):
    db = Session()
    result = db.query(MovideModel).filter(MovideModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message":"Movie deleted successfully"}, status_code=200)