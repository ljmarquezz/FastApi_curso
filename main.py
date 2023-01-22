from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
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
    }
]

class Movie(BaseModel):
    id: Optional[int]=None
    tittle: str
    overview: str
    year: int
    rating: float
    category: str

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>HOLA</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int):
    for item in movies:
        if item['id'] == id:
            return item
    return []

@app.get('/movies/', tags=['movies'])
def get_movie_by_category(category:str):
    return [item for item in movies if item["category"] == category]

@app.post('/movies', tags=["movies"])
def create_movie(movie:Movie):
    movies.append(movie)
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