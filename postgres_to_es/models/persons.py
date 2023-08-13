from typing import List

from .general import UUIDMixin, DateMixin


class MoviesInPerson(UUIDMixin):
    role: str


class Persons(UUIDMixin, DateMixin):
    full_name: str
    films: List[MoviesInPerson]
