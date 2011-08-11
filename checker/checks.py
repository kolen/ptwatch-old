
class UnloadedOSMEntity():
    def __init__(self, type, id):
        self.type = type
        self.id = id

def check_ways(check):
    """
    Check ways for broken paths, fill check.ways_directions_breaks
    """
    last_ends = None
    previous_member = None

    wdb = check.ways_directions_breaks

    for role, member in check.osm_relation.members:
        if role != "":
            continue

        if member.type != "way":
            check.add_error("TYPE_WRONG_OBJECT").objects.append(member)
            continue

        wdb.append([member, "unknown", False])

        if not last_ends:
            last_ends = [member.nodes[0], member.nodes[-1]]
        else:
            matched = False
            for end in last_ends:
                if member.nodes[0] == end:
                    # Forward direction
                    wdb[-1][1] = "forward"
                    last_ends = [ member.nodes[-1] ]
                    assert(not wdb[-2][2])
                    if wdb[-2][1] == "unknown":
                        prev = wdb[-2][0]
                        if prev.nodes[-1] == member.nodes[0]:
                            wdb[-2][1] = "forward"
                        else:
                            wdb[-2][1] = "backward"
                    matched = True
                    break
                elif member.nodes[-1] == end:
                    # Backward direction
                    wdb[-1][1] = "backward"
                    last_ends = [ member.nodes[0] ]
                    assert(not wdb[-2][2])
                    if wdb[-2][1] == "unknown":
                        prev = wdb[-2][0]
                        if prev.nodes[-1] == member.nodes[0]:
                            wdb[-2][1] = "backward"
                        else:
                            wdb[-2][1] = "forward"
                    matched = True
                    break

            if not matched:
                # Mark previous way as break-after
                wdb[-2][2] = True
                last_ends = [member.nodes[0], member.nodes[-1]]


    last_error = False
    for way, direction, breac in wdb:
        assert(True if breac else direction != "unknown")

        if last_error:
            last_error = False
            e = check.add_error("TOPO_BROKEN_ROUTE")
            if direction == "forward":
                e.broken_nodes.append(way.nodes[0])
            elif direction == "backward":
                e.broken_nodes.append(way.nodes[-1])

        if breac:
            e = check.add_error("TOPO_BROKEN_ROUTE")
            if direction == "forward":
                e.broken_nodes.append(way.nodes[-1])
            elif direction == "backward":
                e.broken_nodes.append(way.nodes[0])
            else:
                e.broken_nodes.append(way.nodes[0])
                e.broken_nodes.append(way.nodes[-1])
            last_error = True

        for wc in way_checkers:
            wc(check, way, direction, breac)

def check_stops_order(check):
    stop_ids_on_route = []
    for way, direction, breac in check.ways_directions_breaks:
        stops_ids_on_way = [ node.id for node in way.nodes if node.id in check.stops_ids ]
        if direction == "backward":
            stops_ids_on_way.reverse()

        if (len(stops_ids_on_way) and len(stop_ids_on_route) and
            stop_ids_on_route[-1] == stops_ids_on_way[0]):
            del stop_ids_on_way[0]
        stop_ids_on_route += stops_ids_on_way

    stop_ids_on_route_set = set(stop_ids_on_route)
    stops_off_route = check.stops_ids - stop_ids_on_route_set

    if stops_off_route:
        e = check.add_error("TOPO_STOPS_OUTSIDE_ROUTE")
        e.stops += [UnloadedOSMEntity('node', s) for s in stops_off_route]

    stops_ids_listed = [wdb[0].osm_stop.id for wdb in check.stops_platforms]
    print stop_ids_on_route, "\n-", stops_ids_listed
    assert(len(stop_ids_on_route) == len(stops_ids_listed))
    if stops_ids_listed != stop_ids_on_route:
        check.add_error("TOPO_WRONG_STOPS_ORDER")

def check_oneway(check, way, direction, breac):
    """
    Check if direction on one-way roads is correct
    """
    oneway = way.tags.get('oneway')
    if oneway:
        if oneway in ('yes', 'true', '1'):
            if direction == 'backward':
                check.add_error("TOPO_ONEWAY_WRONG_DIRECTION").wrong_direction_ways.append(way)
        elif oneway in ('-1', 'reverse'):
            if direction == 'forward':
                check.add_error("TOPO_ONEWAY_WRONG_DIRECTION").wrong_direction_ways.append(way)

checks = [check_ways, check_stops_order]

way_checkers = [check_oneway]
