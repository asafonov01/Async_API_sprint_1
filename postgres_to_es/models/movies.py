from typing import List, Optional

from .general import UUIDMixin


class MoviesPerson(UUIDMixin):
    name: str


class Movies(UUIDMixin):
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None
    director: str
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[MoviesPerson]] = None
    writers: Optional[List[MoviesPerson]] = None
