import os
from functools import lru_cache

from pydantic import BaseSettings, Field

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class Settings(BaseSettings):
    keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    astradb_client_id: str = Field(...,
                                   env='ASTRADB_CLIENT_ID')
    astradb_client_secret: str = Field(...,
                                       env='ASTRADB_CLIENT_SECRET')

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
