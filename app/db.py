import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection


from . import config

settings = config.get_settings()


BASE_DIR = pathlib.Path(__file__).resolve().parent

ASTRA_CONNECT_BUNDLE = BASE_DIR/'connect_bundle'/'db_connect.zip'
ASTRADB_CLIENT_ID = settings.astradb_client_id
ASTRADB_CLIENT_SECRET = settings.astradb_client_secret


def get_session():
    cloud_config = {
        'secure_connect_bundle': ASTRA_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(
        ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    return session
