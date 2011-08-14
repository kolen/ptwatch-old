"""
Loads osm xml data. Used for testing.
Not a serious osm xml parser though, does not handle errors
"""

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class Handler(ContentHandler):
    def __init__(self, store):
        self.store = store
        self.obj = None

    def startElement(self, name, attrs):
        if name == "node":
            self.obj = (long(attrs['id']), {}, attrs['lat'], attrs['lon'])
        elif name == "way":
            self.obj = (long(attrs['id']), {}, [])
        elif name == "relation":
            self.obj = (long(attrs['id']), {}, [])
        elif name == "tag":
            self.obj[1][attrs['k']] = attrs['v']
        elif name == "nd":
            self.obj[2].append(long(attrs['ref']))
        elif name == "member":
            self.obj[2].append((long(attrs['ref']), attrs['type'], attrs['role']))

    def endElement(self, name):
        if name == "node":
            self.store.add_node(*self.obj)
        if name == "way":
            self.store.add_way(*self.obj)
        if name == "relation":
            self.store.add_relation(*self.obj)

class Object:
    def __repr__(self):
        return "<OSM %s id=%s>" % (self.type, self.id)

class Node(Object):
    __slots__ = ["id", "tags", "lat", "lon"]
    type = "node"
    def __init__(self, id, tags, lat, lon):
        self.id = id
        self.tags = tags
        self.lat = lat
        self.lon = lon

class Way(Object):
    __slots__ = ["id", "tags", "nodes"]
    type = "way"
    def __init__(self, id, tags, nodes):
        self.id = id
        self.tags = tags
        self.nodes = nodes

class Relation(Object):
    __slots__ = ["id", "tags", "members"]
    type = "relation"
    def __init__(self, id, tags, members):
        self.id = id
        self.tags = tags
        self.members = members

class UnloadedObject(Object):
    """
    OSM entity that exist as member of relation but not retrieved / not saved in xml
    """
    def __init__(self, type, id):
        self.type = type
        self.id = id

class ParsedOsmData():
    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def add_node(self, id, tags, lat, lon):
        self.nodes[id] = Node(id, tags, lat, lon)

    def add_way(self, id, tags, refs):
        self.ways[id] = Way(id, tags, [self.nodes[node_id] for node_id in refs])

    def add_relation(self, id, tags, refs):
        self.relations[id] = Relation(id, tags, [
            (member_role, getattr(self, member_type + "s").get(member_id)
                or UnloadedObject(member_type, member_id))
            for member_id, member_type, member_role in refs
            ])

def load(filename):
    """
    Load osm data. Return (nodes, ways, relations) dicts (id->object).
    """

    data = ParsedOsmData()
    p = make_parser()
    h = Handler(data)
    p.setContentHandler(h)
    p.parse(filename)
    return (data.nodes, data.ways, data.relations)

