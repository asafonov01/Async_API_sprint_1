from typing import Dict, Iterator, List
import logging

from data_transform import transform
from elsasticsearch_loader import ElasticSearchLoader
from models import ExtractIndex
from postgres_extractor import PostgresExtractor
from redis_state import RedisState


logger = logging.getLogger(__name__)


class ETLProcess:

    def __init__(
        self,
        extractor: PostgresExtractor,
        loader: ElasticSearchLoader,
        state: RedisState
    ) -> None:
        self.extractor = extractor
        self.loader = loader
        self.state = state

    def __call__(self, name_table: str):
        """Главный метод ETL, вызывается постоянно в бесконечном цикле.
        В начале получаем дату последнего обновления по названию таблицы.
        Далее отправляем легкий запрос на список индексов.
        Если индексы существуют - обновляем состояние по названию таблицы.
        Если название таблицы не film_work, делаем еще один запрос.
        Отправляем большой запрос на список фильмов с аггрегацией.
        Обрабатываем данные и загружаем в еластик.
        """
        latest_modified: str = self.state.get_latest_modified(name_table)
        array_indeces: List[ExtractIndex] = self.extractor.get_initial_indeces(
            name_table, latest_modified
        )
        if not array_indeces:
            logger.info(f'no new data was found in the {name_table} table')
            return
        new_latest_modified: str = str(array_indeces[-1].modified)
        self.state.set_latest_modified(name_table, new_latest_modified)
        if name_table != 'film_work':
            array_indeces = self.extractor.get_film_work_indeces(
                name_table, array_indeces
            )
        raw_data: List[Dict] = (
            self.extractor.get_full_merged_query(array_indeces)
        )
        data: Iterator[Dict] = transform(raw_data)
        self.loader.load_data(data)
