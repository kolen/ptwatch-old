class Entity:
    def __repr__(self):
        return "<OSM %s id=%s>" % (self.type, self.id)

class Node(Entity):
    __slots__ = ["id", "tags", "lat", "lon"]
    type = "node"
    def __init__(self, id, tags, lat, lon):
        self.id = id
        self.tags = tags
        self.lat = lat
        self.lon = lon

class Way(Entity):
    __slots__ = ["id", "tags", "nodes"]
    type = "way"
    def __init__(self, id, tags, nodes):
        self.id = id
        self.tags = tags
        self.nodes = nodes

class Relation(Entity):
    __slots__ = ["id", "tags", "members"]
    type = "relation"
    def __init__(self, id, tags, members):
        self.id = id
        self.tags = tags
        self.members = members

class UnloadedObject(Entity):
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
