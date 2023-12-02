from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@mail.com":
            raise HTTPException(status_code=401, detail="Invalid User")
            