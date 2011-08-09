
# -*- coding: utf-8 -*-

from tempfile import mkdtemp
import logging
import re
import os.path

from django.test import TestCase
from django.conf import settings
from django.db import connections, transaction

import checker
from models import RouteMaster, RouteOsmStop, Route, OsmStop

class CheckerTest(TestCase):
    fixtures = ["simple.json"]

    def test_unicode_selection(self):
        c = connections['osm'].cursor()
        c.execute("select * from way_tags where v='Ленинский проспект'")
        result = c.fetchall()
        self.assert_(len(result) > 0)
        
        c.execute("select * from relation_tags where relation_id = 380499")
        result = c.fetchall()
        print result
        self.assertEquals(5, len(result))

    def test_unicode_selection2(self):
        c = connections['osm'].cursor()
        c.execute("select * from way_tags where way_id=31290732")
        result = c.fetchall()
        self.assertEquals(8, len(result))

    def test_unicode_selection3(self):
        c = connections['osm'].cursor()
        c.execute("select * from relation_tags where relation_id=1662421")
        result = c.fetchall()
        print "rowcount: %d" % c.rowcount
        self.assertEquals(20, len(result))
        
        
#    def setUp(self):
#        script = open("testdata/pgsimple_schema_0.6.sql").read()
#        script += open("testdata/pgsimple_load_0.6.sql").read()
#        path = os.path.abspath("testdata/import_data")
#        script = re.sub("(?<=FROM ')(?=[a-z_]+\.txt')", path, script)
#        script = script.replace(r"\copy", "copy")
#        c = connections['osm'].cursor()
#        for statement in script.split(';'):
#            c.execute(statement)

    def test_osm_get_tags(self):
        tags = checker.osm_get_tags(380499, "relation")
        self.assertEquals({
            'name': 'Профессиональная – микрорайон "Сомбатхей"',
            'note': 'Правая сторона',
            'ref': '22',
            'route': 'bus',
            'type': 'route',
        }, tags)

    def test_route_fill_from_osm(self):
        route = Route.objects.get(pk=1)
        checker.route_update_check_data(route)

        #get again
        route = RouteMaster.objects.get(pk=2)

        self.assertEquals("22", route.osm_ref)
        self.assertEquals('Профессиональная – микрорайон "Сомбатхей"', route.osm_name)
        self.assertEqual('', route.osm_operator)
        self.assertEqual('', route.osm_colour)
        self.assertEqual(380499, route.osm_relation_id)
        self.assertEqual(False, route.is_vintage)
        self.assertEqial(False, route.is_not_found_in_osm)

