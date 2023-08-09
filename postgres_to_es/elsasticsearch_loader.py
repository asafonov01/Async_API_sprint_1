from typing import Dict, Iterator

import backoff
from conf import BACKOFF_CONFIG
from elasticsearch import Elasticsearch, helpers


class ElasticSearchLoader:

    def __init__(self, es_client, batch_size) -> None:
        self._es_client: Elasticsearch = es_client
        self._batch_size = batch_size

    @backoff.on_exception(**BACKOFF_CONFIG)
    def load_data(self, data: Iterator[Dict]):
        helpers.bulk(
            client=self._es_client,
            actions=data,
            index='movies',
            chunk_size=self._batch_size,
        )
