
from ptwatch.checker import Checker
from ptwatch.osm.pgsimple_loader import load_relation, NotFoundException

def update_route(route):
    if not route.osm_relation_id:
        route.check_result = None
        route.relation_not_found = False
        return

    try:
        relation = load_relation(route.osm_relation_id)
    except NotFoundException:
        route.check_result = None
        route.relation_not_found = True
        return

    result = Checker.check_route(relation, [], "bus")
    route.check_result = result
    route.relation_not_found = False
