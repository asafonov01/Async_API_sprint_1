from contextlib import contextmanager
from elasticsearch import Elasticsearch


@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()


@contextmanager
def elastic_connection(dsn):
    host = dsn.get('host')
    port = dsn.get('port')
    elastic_connection = Elasticsearch(f'http://{host}:{port}')
    try:
        yield elastic_connection
    finally:
        elastic_connection.close()
