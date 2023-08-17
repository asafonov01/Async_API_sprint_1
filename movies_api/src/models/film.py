from typing import Optional

from .base import BaseMoviesModel


class FilmList(BaseMoviesModel):
    title: str
    imdb_rating: Optional[float]


class FilmDetail(FilmList):
    description: Optional[str]
    genre: Optional[list[str]]
    director: Optional[str]
    writers: Optional[list[dict]]
    actors: Optional[list[dict]]
