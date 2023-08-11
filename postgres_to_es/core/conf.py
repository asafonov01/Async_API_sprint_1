import logging
import os

import backoff
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)

DB_TABLES = ['film_work', 'genre', 'person']
ES_INDECES = ['movies', ]  # movies, genres, persons
BATCH_SIZE = 10
SLEEP_TIME = 1


class PostgresConfig(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


class ElasticSeachConfig(BaseModel):
    host: str
    port: int


class RedisConfig(BaseModel):
    host: str
    port: int


PSQL_DSN = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': 'localhost',  # TEST in localhost
    'port': os.environ.get('POSTGRES_PORT'),
}


ES_DSN = {
    'host': 'localhost',  # TEST
    'port': 9200,
}

REDIS_DSN = {
    'host': 'localhost',  # TEST
    'port': 6379,
}

BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "logger": logger,
    "max_tries": 3,
}


pg_config = PostgresConfig(**PSQL_DSN)
es_config = ElasticSeachConfig(**ES_DSN)
redis_config = RedisConfig(**REDIS_DSN)
