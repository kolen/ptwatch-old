
# -*- coding: utf-8 -*-

import unittest
from ptwatch.osm.loader import load

class TestParse(unittest.TestCase):
    TEST_RESOURCES_DIR = "ptwatch/checker/test/resources"
    def setUp(self):
        if not getattr(self, 'data', None):
            self.data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1.osm")

    def test_loaded(self):
        self.assertEquals(3, len(self.data))
        self.assertIsInstance(self.data[0], dict)
        self.assertIsInstance(self.data[1], dict)
        self.assertIsInstance(self.data[2], dict)

    def test_way_tags(self):
        w = self.data[1][33893970]
        self.assertEquals({
            "addr:postcode": "424005",
            "cladr:code": "12000001000014100",
            "cladr:name": u"Карла Либкнехта",
            "cladr:suffix": u"Улица",
            "highway": "tertiary",
            "name": u"улица Карла Либкнехта",
            "trolley_wire": "yes",
        }, w.tags)

    def test_relations1(self):
        r = self.data[2][1660415]
        self.assertEquals(56, len(r.members))
        self.assertEquals(('forward', self.data[1][106233412]), r.members[5])
        self.assertEquals(u"Новый – микрорайон \"Дубки\"", r.tags['name'])

    def test_relations2(self):
        r = self.data[2][380499] #this is relation of new route schema
        self.assertEquals(('platform', self.data[0][1251026055]), r.members[1])
        self.assertEquals(116, len(r.members))
