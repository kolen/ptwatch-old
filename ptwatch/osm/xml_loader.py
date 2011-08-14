from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from entities import ParsedOsmData

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

def load(filename):
    """
    Load osm data from xml. Return (nodes, ways, relations) dicts (id->object).
    """

    data = ParsedOsmData()
    p = make_parser()
    h = Handler(data)
    p.setContentHandler(h)
    p.parse(filename)
    return (data.nodes, data.ways, data.relations)
