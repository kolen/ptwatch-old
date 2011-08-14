
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
                e = Node(id)
            elif type == 'way':
                e = Way(id)
            elif type == 'relation':
                e = Relation(id)
            else:
                raise AttributeError("Invalid type '%s'" % type)
            d[id] = e
            return e
        else:
            return d[id]

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
        members.append(entity)

    nodes_ids = set(str(node.id) for node in store.nodes.itervalues())
    ways_ids = set(str(way.id) for way in store.ways.itervalues())

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
        n.tags[k] = v

    # Load tags for all ways
    c.execute("select way_id, k, v from way_tags where way_id in (%s)" %
        (",".join(ways_ids)))
    for way_id, k, v in c.fetchall():
        w = store.ways[way_id]
        w.tags[k] = v

    return Relation(id, rel_tags, members)
