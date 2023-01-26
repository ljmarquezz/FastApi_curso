from pydantic import BaseModel

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