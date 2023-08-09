from typing import Dict, List

import backoff
from conf import BACKOFF_CONFIG
from models import ElasticFilmwork, ExtractIndex
from psycopg2.extras import DictCursor


class PostgresExtractor:

    def __init__(self, cursor: DictCursor, batch_size: int) -> None:
        self._cursor = cursor
        self._batch_size = batch_size

    @backoff.on_exception(**BACKOFF_CONFIG)
    def get_initial_indeces(
        self,
        name_table: str,
        last_modified: str
    ) -> List[ExtractIndex]:
        """Получение списка индексов по названию таблицы.
        Данные отфильтрованы по дате обновления.
        Данные отсортированы по возрастанию даты обновления.
        """
        self._cursor.execute(f"""
            SELECT id, modified
            FROM content.{name_table}
            WHERE modified > '{last_modified}'
            ORDER BY modified
            LIMIT {self._batch_size};
        """)
        return [ExtractIndex(**i) for i in self._cursor.fetchall()]

    @backoff.on_exception(**BACKOFF_CONFIG)
    def get_film_work_indeces(
        self,
        name_table: str,
        array_indeces: List[ExtractIndex]
    ) -> List[ExtractIndex]:
        """Получение списка индексов фильмов.
        Получаем с помощью индексов промежуточных таблиц.
        Данные отсортированы по возрастанию даты обновления.
        Метод недоступен для индексов film_work.
        """
        string_indeces: str = ', '.join(
            f"'{index.id}'" for index in array_indeces
        )
        self._cursor.execute(f"""
            SELECT fw.id, fw.modified
            FROM content.film_work fw
            LEFT JOIN content.{name_table}_film_work joined
            ON joined.film_work_id = fw.id
            WHERE joined.{name_table}_id IN ({string_indeces})
            ORDER BY fw.modified
            LIMIT {self._batch_size};
        """)
        return [ExtractIndex(**i) for i in self._cursor.fetchall()]

    @backoff.on_exception(**BACKOFF_CONFIG)
    def get_full_merged_query(
        self,
        array_indeces: List[ExtractIndex]
    ) -> List[Dict]:
        """Полный запрос с аггрегацией, пригодный для elastic индекса movies.
        """
        film_work_string_indeces: str = ', '.join(
            f"'{index.id}'" for index in array_indeces
        )
        self._cursor.execute(f"""
            SELECT
                fw.id,
                fw.id as _id,
                fw.rating as imdb_rating,
                ARRAY_AGG(DISTINCT g.name) AS genre,
                fw.title,
                fw.description,
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
            WHERE fw.id IN ({film_work_string_indeces})
            GROUP BY fw.id
            ORDER BY fw.modified
            LIMIT {self._batch_size};
        """)
        # очень тяжело работать с парсингом генераторов
        # особенно при получении начальных индексов, их все равно придется мержить
        return [
            ElasticFilmwork(**data).model_dump()
            for data in self._cursor.fetchall()
        ]
