
def check_ways(check):
    """
    Check ways for broken paths, fill check.ways_directions_breaks
    """
    last_end = None
    last_end_2 = None # Other possible end, if first way encountered.
                      # After next way it will be reset
    previous_member = None

    wdb = check.ways_directions_breaks

    for role, member in check.osm_relation.members:
        if role != "":
            continue

        if member.type != "way":
            check.add_error("TYPE_WRONG_OBJECT").objects.append(member)
            continue

        wdb.append([member, "unknown", False])

        if not last_end:
            last_end = member.nodes[0]
            last_end_2 = member.nodes[-1]
        else:
            while True:
                if member.nodes[0] == last_end:
                    # Forward direction
                    last_end = member.nodes[-1]
                    wdb[-1][1] = "forward"
                    if wdb[-2][1] == "unknown":
                        prev = wdb[-2][0]
                        if prev.nodes[-1] == member.nodes[0]:
                            wdb[-2][1] = "forward"
                        else:
                            wdb[-2][1] = "backward"
                elif member.nodes[-1] == last_end:
                    # Backward direction
                    last_end = member.nodes[0]
                    wdb[-1][1] = "backward"
                    if wdb[-2][1] == "unknown":
                        prev = wdb[-2][0]
                        if prev.nodes[-1] == member.nodes[0]:
                            wdb[-2][1] = "backward"
                        else:
                            wdb[-2][1] = "forward"
                else:
                    if last_end_2:
                        # Continue with trying alternative direction
                        last_end = last_end_2
                        last_end_2 = None
                        continue
                    else:
                        wdb[-1][2] = True

                break

            last_end_2 = None

    for way, direction, breac in wdb:
        if breac:
            e = check.add_error("TOPO_BROKEN_ROUTE")
            if direction == "forward":
                e.broken_nodes.append(way.nodes[-1])
            elif direction == "backward":
                e.broken_nodes.append(way.nodes[0])
            else:
                e.broken_nodes.append(way.nodes[0])
                e.broken_nodes.append(way.nodes[-1])

        for wc in way_checkers:
            wc(check, way, direction, breac)

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

checks = [check_ways]

way_checkers = [check_oneway]
