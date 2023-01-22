from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

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
def create_movie(id:int=Body(), tittle:str=Body(), overview:str=Body(), year:int=Body(), rating:float=Body(), category:str=Body()):
    movies.append(
        {
            'id':id,
        'tittle': tittle,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
        }
    )
    return movies

@app.put("/movies/{id}", tags=["movies"])
def update_movie(id:int, tittle:str=Body(), overview:str=Body(), year:int=Body(), rating:float=Body(), category:str=Body()):
    for item in movies:
        if item['id'] == id:
            item['tittle'] = tittle
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return item
    return []


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return []