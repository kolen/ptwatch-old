
from pyramid.config import global_registries
import pyramid.threadlocal
from entities import Node, Way, Relation, UnloadedEntity

class NotFoundException(Exception):
    pass

class LoadedEntitiesStore():
    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def get_or_create(self, type, id):
        d = getattr(self, type+"s")
        if id not in d:
            if type == 'node':
                e = Node(id, {})
            elif type == 'way':
                e = Way(id, {})
            elif type == 'relation':
                e = Relation(id, {})
            else:
                raise AttributeError("Invalid type '%s'" % type)
            d[id] = e
            return e
        else:
            return d[id]

    def integrity_check(self):
        for node in self.nodes.itervalues():
            if node.lat is None or node.lon is None:
                print "Node %s have invalid lat(%s) or lon(%s)" % (
                    node, node.lat, node.lon
                )
                return False
        for way in self.ways.itervalues():
            if not way.nodes:
                print "Way %s nodes is invalid: %s" % (way, way.nodes)
                return False
        for relation in self.relations.itervalues():
            for role, member in relation.members:
                if not member:
                    print "Member of %s is invalid: %s" % (relation, member)
                    return False

            if member.type == "node":
                if member.id not in self.nodes:
                    print "Member of %s not in list of nodes" % relation
                    return False
            elif member.type == "way":
                if member.id not in self.ways:
                    print "Member of %s not in list of ways" % relation
                    return False

        return True


def load_relation(id):
    """
    Load relation from pgsimple OSM database, with nodes and ways included
    in relation loaded. Nodes contained by ways are also loaded.

    It will not load relations contained in this relation, returning
    UnloadedEntity as child relation object
    """
    try:
        pool = global_registries.last.osm_db_pool
    except AttributeError:
        pool = pyramid.threadlocal.get_current_registry().osm_db_pool
    conn = pool.connection(shareable=False)

    c = conn.cursor()
    c.execute("select id from relations where id=%s", (id,))
    if not c.fetchone():
        raise NotFoundException("Relation %d not found" % id)

    c.execute("select k, v from relation_tags where relation_id=%s", (id,))
    rel_tags = dict(c.fetchall())

    # Load members of relation
    store = LoadedEntitiesStore()
    members = []
    types_map = dict(N='node', W='way', R='relation')
    c.execute("select member_id, member_type, member_role from relation_members"
        " where relation_id=%s order by sequence_id", (id,))
    for m_id, m_type, m_role in c.fetchall():
        m_type = types_map[m_type]

        if m_type == 'relation':
            members.append(UnloadedEntity('relation', m_id))
            next

        entity = store.get_or_create(m_type, m_id)
        members.append((m_role, entity))

    ways_ids = set(str(way.id) for way in store.ways.itervalues())

    # Add nodes to ways
    c.execute("select way_id, node_id from way_nodes"
        " where way_id in (%s) order by way_id, sequence_id" %
        (",".join(ways_ids)))
    for way_id, node_id in c.fetchall():
        w = store.ways[way_id]
        if w.nodes is None:
            w.nodes = []
        w.nodes.append(store.get_or_create('node', node_id))

    nodes_ids = set(str(node.id) for node in store.nodes.itervalues())

    # Load all nodes
    c.execute("select id, ST_Y(geom) lat, ST_X(geom) lon from nodes"
        " where id in (%s)" % (",".join(nodes_ids)))
    for node_id, lat, lon in c.fetchall():
        n = store.nodes[node_id]
        n.lat = lat
        n.lon = lon

    # Load tags for all nodes
    c.execute("select node_id, k, v from node_tags where node_id in (%s)" %
        (",".join(nodes_ids)))
    for node_id, k, v in c.fetchall():
        n = store.nodes[node_id]
        assert(n.id == node_id)
        n.tags[k] = v

    # Load tags for all ways
    c.execute("select way_id, k, v from way_tags where way_id in (%s)" %
        (",".join(ways_ids)))
    for way_id, k, v in c.fetchall():
        w = store.ways[way_id]
        assert(w.id == way_id)
        w.tags[k] = v

    assert(store.integrity_check())

    return Relation(id, rel_tags, members)
