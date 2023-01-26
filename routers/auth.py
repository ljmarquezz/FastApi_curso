from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from schemas.user import User

auth_router = APIRouter()

@auth_router.post('/login', tags=['auth'])
def login(user: User) -> str:
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(content='')