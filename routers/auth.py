from schemas.user import User
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/login", tags=['Auth'], response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "123456":
        token = create_token(data=user.model_dump())
        result = JSONResponse(content={"message": "Usuario autenticado correctamente", "token": token}, status_code=200)
    else:
        result = JSONResponse(content={"message": "Unauthorized"}, status_code=401)
    return result