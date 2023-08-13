import logging
from typing import Dict, Iterator, List

from etl.data_transform import transform
from etl.elsasticsearch_loader import ElasticSearchLoader
from etl.postgres_extractors import PostgresExtractor
from etl.redis_state import RedisState


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

    def __call__(self, index):
        state_key = index
        latest_modified: str = self.state.get_latest_modified(state_key)
        raw_data = self.extractor.extract_data(index, latest_modified)
        if not raw_data:
            logger.info(f'no new data was found for ES index {index}')
            return
        new_latest_modified: str = str(raw_data[-1]['modified'])
        self.state.set_latest_modified(state_key, new_latest_modified)
        data = transform(raw_data)
        self.loader.load_data(index, data)
