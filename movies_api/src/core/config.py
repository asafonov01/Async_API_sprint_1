import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

PROJECT_NAME = 'movies_api'

REDIS_HOST = os.getenv('...', '127.0.0.1')
REDIS_PORT = int(os.getenv('...', 6379))

ELASTIC_HOST = os.getenv('...', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('...', 9200))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
