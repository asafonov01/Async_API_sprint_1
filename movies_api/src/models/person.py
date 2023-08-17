from typing import Optional, Any

from .base import BaseMoviesModel


class Person(BaseMoviesModel):
    full_name: str
    films: Optional[list[dict[str, Any]]]
