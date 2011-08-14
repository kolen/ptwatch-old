
from unittest import TestCase
from DBUtils.PooledDB import PooledDB
import psycopg2
from pyramid import testing

DB_CONFIG = dict(
    database='osm_small',
    user='postgres',
    password='123',
    host='localhost',
)

class OSMPGSQLTestCase(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.registry.osm_db_pool = PooledDB(psycopg2,
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
        )
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

    def tearDown(self):
        testing.tearDown()