
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
