from typing import List, Optional

from .base import BaseMoviesModel


class FilmList(BaseMoviesModel):
    title: str
    imdb_rating: Optional[float]


class FilmDetail(FilmList):
    description: Optional[str]
    genre: Optional[List[str]]
    director: Optional[str]
    writers: Optional[List[dict]]
    actors: Optional[List[dict]]
