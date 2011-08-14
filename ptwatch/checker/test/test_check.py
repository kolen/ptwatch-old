
from unittest import TestCase
from ptwatch.osm.xml_loader import load
from ptwatch.checker import Checker

class TestCheck(TestCase):
    TEST_RESOURCES_DIR = "ptwatch/checker/test/resources"

    def testCheck1(self):
        data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1.osm")
        results = Checker.check_route(data[2][380499], [], "bus")
        self.assertEquals(["TOPO_ONEWAY_WRONG_DIRECTION"], results.errors.keys())
        self.assertEquals([31746305], [e.id for e in results.errors["TOPO_ONEWAY_WRONG_DIRECTION"].wrong_direction_ways])

    def testCheck1OnewayFixed(self):
        data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1_oneway_fixed.osm")
        results = Checker.check_route(data[2][380499], [], "bus")
        self.assertEquals({}, results.errors)

    def testRoute380499Broken(self):
        data = load(self.TEST_RESOURCES_DIR+"/route_380499_broken.osm")
        results = Checker.check_route(data[2][380499], [], "bus")
        self.assertEquals(set(["TOPO_BROKEN_ROUTE", "TOPO_STOPS_OUTSIDE_ROUTE"]), set(results.errors.keys()))
        self.assertEquals([
            1365747987L, 324160729L, 335945606L, -1286L, 635942387L, 324169952L, 335945607L,
            ], [e.id for e in results.errors["TOPO_BROKEN_ROUTE"].broken_nodes])