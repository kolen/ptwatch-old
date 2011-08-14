from uuid import uuid4
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

class PTWatch(PersistentMapping):
    __name__ = None
    __parent__ = None

class Cities(PersistentMapping):
    pass

class City(Persistent):
    def __init__(self):
        name = ""
        country = ""
        osm_entities = PersistentList()
        routes = RouteMasters

class RouteMasters(Persistent):
    def __init__(self, city):
        self.__name__ = "routes"
        self.__parent__ = city

class RouteMaster(PersistentMapping):
    def __init__(self, routemasters):
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

class Route(Persistent):
    def __init__(self, route_master):
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
        import transaction
        transaction.commit()
    return zodb_root['app_root']
