from .general import UUIDMixin, DateMixin


class Genres(UUIDMixin, DateMixin):
    name: str
