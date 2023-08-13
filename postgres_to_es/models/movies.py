from typing import List, Optional
from .general import UUIDMixin, DateMixin


class PersonsInMovies(UUIDMixin):
    name: str


class Movies(UUIDMixin, DateMixin):
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None
    director: str
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[PersonsInMovies]] = None
    writers: Optional[List[PersonsInMovies]] = None
