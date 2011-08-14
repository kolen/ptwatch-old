
from unittest import TestCase
from DBUtils.PooledDB import PooledDB
import psycopg2
from pyramid import testing
import pgsimple_loader

DB_CONFIG = dict(
    database='osm_small',
    user='postgres',
    password='123',
    host='localhost',
)

class TestLoad(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.registry.osm_db_pool = PooledDB(psycopg2,
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
        )

    def tearDown(self):
        testing.tearDown()

    def testLoad1(self):
        rel = pgsimple_loader.load_relation(380499)

        self.assertEquals(dict(ref="22", route="bus", type="route"), rel.tags)
        self.assertEquals(82, len(rel.members))
        for role, member in rel.members:
            if role == 'node':
                self.assertMoreThan(50, member.lat)