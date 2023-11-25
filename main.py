from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def message():
    return HTMLResponse(content = "<h1>Hola Mundo!!!!</h1>")