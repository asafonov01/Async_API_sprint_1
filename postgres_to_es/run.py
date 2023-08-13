import logging
import time

from core.conf import (BATCH_SIZE, SLEEP_TIME, es_config, pg_config,
                       redis_config, ES_INDECES)
from core.connection_managers import (elastic_connection, pg_connection,
                                      redis_connection)
from etl.elsasticsearch_loader import ElasticSearchLoader
from etl.etl_process import ETLProcess
from etl.postgres_extractors import PostgresExtractor
from etl.redis_state import RedisState


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s, %(levelname)s: %(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)

    with (
        pg_connection(pg_config.model_dump()) as pg_conn,
        pg_conn.cursor() as pg_cur,
        elastic_connection(es_config.model_dump()) as es_client,
        redis_connection(redis_config.model_dump()) as redis_client,
    ):
        state = RedisState(redis_client)
        extractor = PostgresExtractor(pg_cur, BATCH_SIZE)
        loader = ElasticSearchLoader(es_client, BATCH_SIZE)
        etl = ETLProcess(extractor, loader, state)
        while True:
            for index in ES_INDECES:
                try:
                    etl(index)
                except Exception as e:
                    logger.error(e)
            logger.info(f'wait for {SLEEP_TIME} seconds ...')
            time.sleep(SLEEP_TIME)
