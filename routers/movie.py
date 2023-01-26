from fastapi import APIRouter, Body, Path, Query, Request, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(category:str = Query(min_length=5, max_length=20)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=200, content={'message':'No hay peliculas de esa categoria'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def create_movie(movie:Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=200, content={'message':'Se ha registrado la pelicula'})

@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def update_movie(id:int, movie:Movie) -> dict:
    db=Session()
    result = MovieService(db).update_movie(id, movie)
    if result:
        return JSONResponse(status_code=200,content={'message':'Se ha actualizado la pelicula'})
    else:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})

@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, dependencies=[Depends(JWTBearer())])
def delete_movie(id:int) -> dict:
    db=Session()
    result = MovieService(db).delete_movie(id)
    if result:
        return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula'})
    else:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})