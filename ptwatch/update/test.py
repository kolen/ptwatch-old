from ptwatch.test_with_osm_pgsql import OSMPGSQLTestCase
from ptwatch.update import update_route
from ptwatch.models import Route

class TestUpdate(OSMPGSQLTestCase):
    def testUpdateNotExist(self):
        route = Route(None)
        route.osm_relation_id = 10
        update_route(route)
        self.assertTrue(route.relation_not_found)
        self.assertIsNone(route.check_result)

    def testUpdate380499(self):
        route = Route(None)
        route.osm_relation_id = 380499
        update_route(route)
        self.assertFalse(route.relation_not_found)
        self.assertIsNotNone(route.check_result)
