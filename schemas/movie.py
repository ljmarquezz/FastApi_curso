
from pydantic import BaseModel, Field
from typing import Optional

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
                'category': 'Categoria'
            }
        }