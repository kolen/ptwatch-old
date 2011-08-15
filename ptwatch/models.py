from uuid import uuid4
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

allowed_types = ['bus', 'trolleybus', 'share_taxi', 'tram']

error_levels = dict(ok=0, notice=1, warning=2, error=3, empty=4)

class PTWatch(PersistentMapping):
    __name__ = None
    __parent__ = None

class Cities(PersistentMapping):
    pass

class City(Persistent):
    def __init__(self):
        self.name = ""
        self.country = ""
        self.osm_entities = PersistentList()
        self.route_masters = RouteMasters(self)

class RouteMasters(PersistentMapping):
    def __init__(self, city):
        PersistentMapping.__init__(self)
        self.__name__ = "routes"
        self.__parent__ = city

class RouteMaster(PersistentMapping):
    def __init__(self, routemasters):
        PersistentMapping.__init__(self)
        self._last = 0
        self.__parent__ = routemasters

        self.osm_relation_id = None  # OSM relation id (type=route_master)
        self.ref = ""
        self.name = "" # Name, i.e. "Tarkhanovo - Turunovo"
        self.type = "" # Type, i.e. bus

    def new(self):
        self._last += 1
        r = Route(self)
        r.__name__ = self._last
        self[self._last] = r
        return r

    @property
    def status(self):
        return max((route.status for route in self.itervalues()),
                   key = lambda x: error_levels[x]) or "empty"

    @property
    def manual_status(self):
        ms = "checked"
        for route in self.itervalues():
            if route.manual_status == "unknown":
                ms = "unknown"
            elif route.manual_status == "error":
                return "error"
        return ms

class Route(Persistent):
    def __init__(self, route_master):
        Persistent.__init__(self)
        self.__parent__ = route_master

        self.osm_relation_id = None  # OSM relation id (type=route)
        self.ref = "" # Ref, i.e. "22"
        self.name = "" # Name, i.e. "Tarkhanovo - Turunovo"
        self.stops = [] # Stops reference

        self.check_result = None
        self.status = "empty" # empty, vintage, notice, warning, error
        self.manual_status = "unknown" # unknown, checked, error
        self.relation_not_found = False

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = PTWatch()
        cities = Cities()
        cities.__name__ = 'cities'
        cities.__parent__ = app_root
        app_root['cities'] = cities
        zodb_root['app_root'] = app_root

        c = City()
        c.name = "Test City"
        c.country = "Inner Nepal"
        c.__parent__ = cities
        c.__name__ = "Test City"
        cities["Test City"] = c

        import transaction
        transaction.commit()
    return zodb_root['app_root']
