import logging
import time

from core.conf import (BATCH_SIZE, DB_TABLES, SLEEP_TIME, es_config, pg_config,
                       redis_config, ES_INDECES)
from core.connection_managers import (elastic_connection, pg_connection,
                                      redis_connection)
from etl.elsasticsearch_loader import ElasticSearchLoader
from etl.etl_process import ETLProcess
from etl.postgres_extractors import (FilmworkPostgresExtractor,
                                     GenrePostgresExtractor,
                                     PersonPostgresExtractor)
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
        extracotrs_mapping = {
            'movies': FilmworkPostgresExtractor,
            'genres': GenrePostgresExtractor,
            'persons': PersonPostgresExtractor,
        }
        state = RedisState(redis_client)
        while True:
            for index in ES_INDECES:
                extractor = extracotrs_mapping[index](pg_cur, BATCH_SIZE)
                loader = ElasticSearchLoader(index, es_client, BATCH_SIZE)
                for table_name in DB_TABLES:
                    try:
                        etl = ETLProcess(index, extractor, loader, state)
                        etl(table_name)
                    except Exception:
                        logger.error(f'falied to extract data from {table_name} for ES index {index}')

            logger.info(f'wait for {SLEEP_TIME} seconds ...')
            time.sleep(SLEEP_TIME)
