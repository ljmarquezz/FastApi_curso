from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = 'Learning FastAPI'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

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

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com' or data['password'] != 'admin':
            raise HTTPException(status_code=403, detail='Credenciales invalidas')


class Movie(BaseModel):
    id: Optional[int]=None
    tittle: str = Field(max_length=50, min_length=5)
    overview: str = Field(min_length=10)
    year: int = Field(le=2023)
    rating: float = Field(ge=1,le=10.0)
    category: str = Field(max_length=20)

    class Config:
        schema_extra = {
            'example': {
                'id':1,
                'tittle': 'Titulo de la pelicula',
                'overview': 'Sinopsis de la pelicula',
                'year':2023,
                'rating': 5.0,
                'category': 'Categoria de la pelicula'
            }
        }

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>HOLA</h1>')

@app.post('/login', tags=['auth'])
def login(user: User) -> str:
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(content='')

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(category:str = Query(min_length=5, max_length=20)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=200, content={'message':'No hay peliculas de esa categoria'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se ha registrado la pelicula'})

@app.put("/movies/{id}", tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def update_movie(id:int, movie:Movie) -> dict:
    db=Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        result.tittle = movie.tittle
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()
        return JSONResponse(status_code=200,content={'message':'Se ha actualizado la pelicula'})
    else:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})

@app.delete("/movies/{id}", tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def delete_movie(id:int) -> dict:
    db=Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula'})
    else:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})