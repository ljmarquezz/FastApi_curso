from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = 'Learning FastAPI'
app.version = '0.0.1'

movies = [
    {
        'id':1,
        'tittle': 'Spiderman',
        'overview': 'Peter Parker fue mordido por una arana y ahora tiene superpoderes',
        'year': 2017,
        'rating': 7.2,
        'category': 'accion'
    },
    {
        'id':2,
        'tittle': 'El gato con botas',
        'overview': 'Antonio Banderas hace la voz de un gato muy mono',
        'year': 2022,
        'rating': 7.9,
        'category': 'animacion'
    },
    {
        'id':3,
        'tittle': 'Iron Man',
        'overview': 'Un multimillonario se hace una armadura y decide luchar contra el crimen en el mundo',
        'year': 2008,
        'rating': 8.5,
        'category': 'accion'
    }
]

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

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(category:str = Query(min_length=5, max_length=20)) -> List[Movie]:
    res = list(filter(lambda item:item['category']==category, movies))
    return JSONResponse(content=res)

@app.post('/movies', tags=["movies"], response_model=dict)
def create_movie(movie:Movie) -> dict:
    movies.append(dict(movie))
    return JSONResponse(content={'message':'Se ha registrado la pelicula'})

@app.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id:int, movie:Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['tittle'] = movie.tittle
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={'message':'Pelicula actualizada'})
    return JSONResponse(status_code=404, content=[])

@app.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={'message':'Se ha eliminado la pelicula'})
    return JSONResponse(status_code=404, content=[])