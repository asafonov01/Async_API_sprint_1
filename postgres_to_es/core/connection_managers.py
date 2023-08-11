from contextlib import contextmanager
from typing import Dict, Iterator

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor
from redis import Redis


@contextmanager
def pg_connection(dsn: Dict[str, str]):
    pg_conn = psycopg2.connect(**dsn, cursor_factory=DictCursor)
    try:
        yield pg_conn
    finally:
        pg_conn.close()


@contextmanager
def elastic_connection(dsn):
    host = dsn.get('host')
    port = dsn.get('port')
    elastic_connection = Elasticsearch(f'http://{host}:{port}')
    try:
        yield elastic_connection
    finally:
        elastic_connection.close()


@contextmanager
def redis_connection(redis_config: Dict[str, str]) -> Iterator[Redis]:
    client = Redis(**redis_config)
    try:
        yield client
    finally:
        client.close()
