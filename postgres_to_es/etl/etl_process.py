import logging
from typing import Dict, Iterator, List

from etl.data_transform import transform
from etl.elsasticsearch_loader import ElasticSearchLoader
from etl.postgres_extractors import BasePostgresExtractor
from etl.redis_state import BaseState
from models.general import ExtractedIndex

logger = logging.getLogger(__name__)


class ETLProcess:

    def __init__(
        self,
        index: str,
        extractor: BasePostgresExtractor,
        loader: ElasticSearchLoader,
        state: BaseState
    ) -> None:
        self.index = index
        self.extractor = extractor
        self.loader = loader
        self.state = state

    def __call__(self, name_table: str):
        state_key = f'{self.index}_{name_table}'
        es_postgres_mapping = {
            'movies': 'film_work',
            'genres': 'genre',
            'persons': 'person'
        }
        latest_modified: str = self.state.get_latest_modified(state_key)
        array_indeces: List[ExtractedIndex] = self.extractor.get_initial_indeces(
            name_table, latest_modified
        )
        if not array_indeces:
            logger.info(f'no new data was found in the {name_table} table for ES index {self.index}')
            return
        new_latest_modified: str = str(array_indeces[-1].modified)
        self.state.set_latest_modified(state_key, new_latest_modified)
        if name_table != es_postgres_mapping[self.index]:
            array_indeces = self.extractor.get_joined_indeces(
                name_table, array_indeces
            )
        raw_data: List[Dict] = (
            self.extractor.get_full_merged_query(array_indeces)
        )
        data: Iterator[Dict] = transform(raw_data)
        self.loader.load_data(data)
