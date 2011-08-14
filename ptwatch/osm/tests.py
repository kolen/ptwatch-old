
# -*- coding: utf-8 -*-

from ptwatch.test_with_osm_pgsql import OSMPGSQLTestCase
import pgsimple_loader

class TestLoad(OSMPGSQLTestCase):
    def testLoadRoute380499(self):
        rel = pgsimple_loader.load_relation(380499)

        self.assertEquals(dict(ref="22", route="bus", type="route"), rel.tags)
        self.assertEquals(82, len(rel.members))
        for role, member in rel.members:
            if role == 'node':
                self.assertIsInstance(member.lat, float)
                self.assertIsInstance(member.lon, float)
            if role == 'way':
                self.assertIsNotNone(member.nodes)
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
