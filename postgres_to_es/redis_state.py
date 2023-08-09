from datetime import datetime

import backoff
from conf import BACKOFF_CONFIG, DB_TABLES
from redis import Redis


class RedisState:
    def __init__(self, client: Redis) -> None:
        self.redis_client = client

    @backoff.on_exception(**BACKOFF_CONFIG)
    def get_latest_modified(self, table_name: str) -> str:
        """Получить значение последнего обновления."""
        latest_modified: bytes = self.redis_client.get(table_name)
        if not latest_modified:
            return str(datetime.min)
        return latest_modified.decode()

    @backoff.on_exception(**BACKOFF_CONFIG)
    def set_latest_modified(
        self,
        table_name: str,
        latest_modified: str
    ) -> None:
        """Установить значение последнего обновления."""
        self.redis_client.set(table_name, latest_modified.encode())

    def _delete_all_keys(self) -> None:
        """Удаление всех ключей."""
        for i in DB_TABLES:
            self.redis_client.delete(i)
