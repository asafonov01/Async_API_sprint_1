from typing import Dict, List

import backoff
from psycopg2.extras import DictCursor

from core.conf import BACKOFF_CONFIG
from models.movies import Movies
from models.genres import Genres
from models.persons import Persons


class PostgresExtractor:
    def __init__(self, cursor: DictCursor, batch_size: int) -> None:
        self._cursor = cursor
        self._batch_size = batch_size

    @backoff.on_exception(**BACKOFF_CONFIG)
    def extract_data(
        self,
        index,
        last_modified,
    ) -> List[Dict]:
        extract_mapping = {
            'movies': self.movies_query,
            'genres': self.genres_query,
            'persons': self.persons_query,
        }
        return extract_mapping[index](last_modified)

    def movies_query(self, last_modified):
        self._cursor.execute(f"""
            SELECT
                fw.id,
                fw.rating as imdb_rating,
                ARRAY_AGG(DISTINCT g.name) AS genre,
                fw.title,
                fw.description,
                GREATEST(fw.modified, MAX(p.modified), MAX(g.modified)) AS modified,
                COALESCE(STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE pfw.role = 'director'), '') AS director,
                ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
                ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
                ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
                ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE
                GREATEST(fw.modified, p.modified, g.modified) > '{last_modified}'
            GROUP BY fw.id
            ORDER BY modified
            LIMIT {self._batch_size};
        """)
        return [
            Movies(**data).model_dump()
            for data in self._cursor.fetchall()
        ]

    def genres_query(self, last_modified):
        self._cursor.execute(f"""
            SELECT
                g.id,
                g.name,
                g.modified
            FROM content.genre g
            WHERE
                g.modified > '{last_modified}'
            GROUP BY g.id
            ORDER BY g.modified
            LIMIT {self._batch_size};
        """)
        return [
            Genres(**data).model_dump()
            for data in self._cursor.fetchall()
        ]

    def persons_query(self, last_modified):
        self._cursor.execute(f"""
            SELECT
                p.id,
                p.full_name,
                p.modified,
                ARRAY_AGG(DISTINCT jsonb_build_object('id', pfw.film_work_id, 'role', pfw.role)) FILTER (WHERE p.id = pfw.person_id) AS films
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
            WHERE
                p.modified > '{last_modified}'
            GROUP BY p.id
            ORDER BY p.modified
            LIMIT {self._batch_size};
        """)
        return [
            Persons(**data).model_dump()
            for data in self._cursor.fetchall()
        ]
