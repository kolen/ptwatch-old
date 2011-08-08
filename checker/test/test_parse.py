
# -*- coding: utf-8 -*-

import unittest
from osm.loader import load

class TestParse(unittest.TestCase):
    TEST_RESOURCES_DIR = "checker/test/resources"
    def setUp(self):
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
            "cladr:suffix": "Улица",
            "highway": "tertiary",
            "name": "улица Карла Либкнехта",
            "trolley_wire": "yes",
        }, w)
