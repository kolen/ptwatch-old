
from unittest import TestCase
from osm.loader import load
import checker

class TestCheck(TestCase):
    TEST_RESOURCES_DIR = "checker/test/resources"
    def setUp(self):
        self.data = load(self.TEST_RESOURCES_DIR+"/yoshkar-ola_1.osm")

    def testCheck1(self):
        results = checker.Checker.check_route_variant(self.data[2][380499], [], "bus")
        self.assertEquals(set(), results.errors)