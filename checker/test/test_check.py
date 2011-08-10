
from unittest import TestCase
from osm.loader import load
import checker

class TestCheck(TestCase):
    TEST_RESOURCES_DIR = "checker/test/resources"

    def testCheck1(self):
        data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1.osm")
        results = checker.Checker.check_route_variant(data[2][380499], [], "bus")
        self.assertEquals(["TOPO_ONEWAY_WRONG_DIRECTION"], results.errors.keys())
        self.assertEquals([31746305], [e.id for e in results.errors["TOPO_ONEWAY_WRONG_DIRECTION"].wrong_direction_ways])

    def testCheck1OnewayFixed(self):
        data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1_oneway_fixed.osm")
        results = checker.Checker.check_route_variant(data[2][380499], [], "bus")
        self.assertEquals({}, results.errors)

    def testRoute380499Broken(self):
        data = load(self.TEST_RESOURCES_DIR+"/route_380499_broken.osm")
        results = checker.Checker.check_route_variant(data[2][380499], [], "bus")
        self.assertEquals(["TOPO_BROKEN_ROUTE"], results.errors.keys())
        self.assertEquals([
            1365747987L, 324160729L, 335945606L, -1286L, 635942387L, 324169952L, 335945607L,
            ], [e.id for e in results.errors["TOPO_BROKEN_ROUTE"].broken_nodes])