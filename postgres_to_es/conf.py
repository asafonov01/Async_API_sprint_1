import logging
import os

import backoff
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

logger = logging.getLogger(__name__)

DB_TABLES = ['film_work', 'genre', 'person']
BATCH_SIZE = 100
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
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT'),
}


ES_DSN = {
    'host': os.environ.get('ES_HOST'),
    'port': os.environ.get('ES_PORT'),
}

REDIS_DSN = {
    'host': os.environ.get('REDIS_HOST'),
    'port': os.environ.get('REDIS_PORT'),
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
