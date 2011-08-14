
# -*- coding: utf-8 -*-

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
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

    def tearDown(self):
        testing.tearDown()

    def testLoadRoute380499(self):
        rel = pgsimple_loader.load_relation(380499)

        self.assertEquals(dict(ref="22", route="bus", type="route"), rel.tags)
        self.assertEquals(82, len(rel.members))
        for role, member in rel.members:
            if role == 'node':
                self.assertIsInstance(member.lat, float)
                self.assertIsInstance(member.lon, float)
            if role == 'way':
                for role2, member2 in member.nodes:
                    self.assertIsInstance(member.lat, float)
                    self.assertIsInstance(member.lon, float)
            self.assertIsInstance(member.tags, dict)

        self.assertEquals("forward", rel.members[2][0])
        self.assertEquals(42440506, rel.members[2][1].id)
        self.assertEquals("way", rel.members[2][1].type)
        self.assertEquals(dict(highway="bus_stop"), rel.members[13][1].tags)

        self.assertEquals(48522817, rel.members[0][1].id)
        self.assertEquals("way", rel.members[0][1].type)

        self.assertEquals({
            "addr:postcode": u"424000",
            "cladr:code": u"12000001000012000",
            "cladr:name": u"Красноармейская",
            "cladr:suffix": u"Улица",
            "highway": u"secondary",
            "name": u"Красноармейская улица",
            "name:ru": u"ул. Красноармейская",
            "trolley_wire": u"yes",
        }, rel.members[0][1].tags)

    def testLoadNotFound(self):
        self.assertRaises(pgsimple_loader.NotFoundException,
            pgsimple_loader.load_relation, 278374892734)
