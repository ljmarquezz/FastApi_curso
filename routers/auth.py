from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

auth_router = APIRouter()

class User(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra = {
            'example': {
                'email':'example@email.com',
                'password':'your password'
            }
        }

@auth_router.post('/login', tags=['auth'])
def login(user: User) -> str:
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(content='')