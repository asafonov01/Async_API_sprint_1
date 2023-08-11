from typing import Dict, Generator

import backoff
from elasticsearch import Elasticsearch, helpers

from core.conf import BACKOFF_CONFIG


class ElasticSearchLoader:

    def __init__(
        self,
        index: str,
        es_client: Elasticsearch,
        batch_size: int
    ) -> None:
        self.index = index
        self._es_client = es_client
        self._batch_size = batch_size

    @backoff.on_exception(**BACKOFF_CONFIG)
    def load_data(self, data: Generator[Dict, None, None]):
        helpers.bulk(
            client=self._es_client,
            actions=data,
            index=self.index,
            chunk_size=self._batch_size,
        )
