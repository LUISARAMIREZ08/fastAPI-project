from fastapi import FastAPI

from fastapi.responses import HTMLResponse

from config.database import engine, Base

from middlewares.error_handler import ErrorHandler

from routers.movie import movie_router
from routers.auth import auth_router

app = FastAPI()

app.title = "Mi primer aplicacion de Peliculas con FastAPI"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

    
@app.get("/",tags=['home'])
def message():
    return HTMLResponse(content = "<h1>Hola Mundo!!!!</h1>")



