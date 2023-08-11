from typing import Generator, List

from models.movies import Movies


def transform(raw_data: List[Movies]) -> Generator[Movies, None, None]:
    """Добавляем id эластика, чтобы повторяющиеся данные перезаписывались."""
    for film in raw_data:
        film['_id'] = film['id']
        yield film
