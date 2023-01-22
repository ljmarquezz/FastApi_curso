from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int = Path(ge=1)):
    for item in movies:
        if item['id'] == id:
            return item
    return []

@app.get('/movies/', tags=['movies'])
def get_movie_by_category(category:str = Query(min_length=5, max_length=20)):
    return list(filter(lambda item:item['category']==category, movies))

@app.post('/movies', tags=["movies"])
def create_movie(movie:Movie):
    movies.append(dict(movie))
    return movies

@app.put("/movies/{id}", tags=["movies"])
def update_movie(id:int, movie:Movie):
    for item in movies:
        if item['id'] == id:
            item['tittle'] = movie.tittle
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return item
    return []


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return []