from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: UUID


class ElasticPerson(UUIDMixin):
    name: str


class ElasticFilmwork(UUIDMixin):
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None
    director: str
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[ElasticPerson]] = None
    writers: Optional[List[ElasticPerson]] = None


class ExtractIndex(UUIDMixin):
    modified: datetime
