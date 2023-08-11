from typing import Optional, List, Dict, Any

from .base import BaseMoviesModel


class Person(BaseMoviesModel):
    full_name: str
    films: Optional[List[Dict[str, Any]]]
