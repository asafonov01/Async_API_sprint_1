from typing import Iterator, List

from models import ElasticFilmwork


def transform(raw_data: List[ElasticFilmwork]) -> Iterator[ElasticFilmwork]:
    """Добавляем id эластика, чтобы повторяющиеся данные перезаписывались."""
    for film in raw_data:
        film['_id'] = film['id']
        yield film
