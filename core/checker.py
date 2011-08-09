
from django.db import connections, transaction

def osm_get_tags(osm_id, osm_type):
    if osm_type not in ["node", "way", "relation"]:
        raise TypeError("osm_type can be only node, way or relation")

    c = connections['osm'].cursor()
    c.execute("select k, v from %s_tags where %s_id = %%s" % (osm_type, osm_type), [osm_id])
    result = c.fetchall()
    print result
    return dict(
        (row[0], row[1])
        for row in result)

def route_clear_osm_data(route):
    route.osm_ref = ""
    route.osm_name = ""
    route.osm_operator = ""
    route.osm_colour = ""
    route.osm_relation_id = None
    route.is_vintage = False
    route.osm_stops = []

def route_fill_osm_tags(route, tags):
    # TODO: validate
    route.osm_ref = tags.get('ref', '')
    route.osm_name = tags.get('name', '')
    route.osm_operator = tags.get('operator', '')
    route.osm_colour = tags.get('colour', '')

def route_update_check_data(route):
    """
    Check route using information from OSM, updating all check data
    """

    if not route.osm_relation_id:
        route_clear_osm_data(route)
        route.save()
        return

    c = connections['osm'].cursor()
    c.execute("select * from relations where id=%s", [route.osm_relation_id])
    osm_relation = c.fetchone()
    if not osm_relation:
        route_clear_osm_data(route)
        route.is_not_found_in_osm = True
        route.save()

    osm_relation_tags = osm_get_tags(route.osm_relation_id, 'relation')
    route_fill_osm_tags(route, osm_relation_tags)
