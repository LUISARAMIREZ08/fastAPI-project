from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from pydantic import BaseModel, Field
import time
from typing import Optional, List 
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

from config.database import Session, engine, Base
from models.movie import Movie as MovideModel
from fastapi.encoders import jsonable_encoder

from middlewares.jwt_bearer import JWTBearer
from middlewares.error_handler import ErrorHandler


app = FastAPI()

app.title = "Mi primer aplicacion de Peliculas"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str
    password:str

    
@app.get("/",tags=['home'])
def message():
    return HTMLResponse(content = "<h1>Hola Mundo!!!!</h1>")


@app.post("/login",tags=['auth'], response_model=dict,status_code=200)
def login(user:User):
    if user.email == "admin@mail.com" and user.password == "1234567890":
        token = create_token(data={"user":user.model_dump()})
        result = JSONResponse(content ={"token":token},status_code=200)
    else:
        result = JSONResponse(content={"message":"Invalid credentials"},status_code=401)
    return result