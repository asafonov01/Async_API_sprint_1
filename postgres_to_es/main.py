import logging
import time

import psycopg2
from redis import Redis
from psycopg2.extras import DictCursor

from conf import (BATCH_SIZE, DB_TABLES, pg_config, es_config, redis_config,
                  SLEEP_TIME)
from connection_managers import closing, elastic_connection
from elsasticsearch_loader import ElasticSearchLoader
from etl import ETLProcess
from postgres_extractor import PostgresExtractor
from redis_state import RedisState


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s, %(levelname)s: %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)

    pg_conn = psycopg2.connect(
        **pg_config.model_dump(),
        cursor_factory=DictCursor
    )
    redis_connection = Redis(**redis_config.model_dump())

    with (
        closing(pg_conn) as pg_conn,
        pg_conn.cursor() as pg_cur,
        closing(redis_connection) as redis_client,
        elastic_connection(es_config.model_dump()) as es_client,
    ):
        extractor = PostgresExtractor(pg_cur, BATCH_SIZE)
        loader = ElasticSearchLoader(es_client, BATCH_SIZE)
        state = RedisState(redis_client)
        while True:
            for table_name in DB_TABLES:
                try:
                    etl = ETLProcess(extractor, loader, state)
                    etl(table_name)
                except Exception:
                    logger.error(f'falied to extract data from {table_name}')

            logger.info(f'wait for {SLEEP_TIME} seconds ...')
            time.sleep(SLEEP_TIME)
