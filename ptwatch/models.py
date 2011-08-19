import transaction
import UserDict
from sqlalchemy import Column, Boolean, Integer, BigInteger, String, Text
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import IntegrityError
from zope.sqlalchemy import ZopeTransactionExtension

allowed_types = ['bus', 'trolleybus', 'share_taxi', 'tram']

error_levels = dict(ok=0, notice=1, warning=2, error=3, empty=4)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
Base = declarative_base()

_root_ptwatch = None

def _keyerror_if_none(f):
    def wrap(self, item):
        ret = f(self, item)
        if ret is None:
            raise KeyError()
        else:
            return ret
    return wrap

class PTWatch(dict):
    __name__ = None
    __parent__ = None

    def __init__(self):
        self['cities'] = Cities()
        self['cities'].__parent__ = self

class Cities():
    __name__ = "cities"

    @_keyerror_if_none
    def __getitem__(self, item):
        session = DBSession()
        return session.query(City).filter_by(urlname=item).first()

class City(Base, UserDict.DictMixin):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    urlname = Column(String, unique=True)

    route_masters = relationship("RouteMaster", backref="city")

    @property
    def __name__(self):
        return self.urlname

    @property
    def __parent__(self):
        return get_root()['cities']

    def __getitem__(self, key):
        if key in allowed_types:
            if not getattr(self, "_keys", None):
                self._keys = {}
            if not self._keys.has_key(key):
                self._keys[key] = RouteMasters(key, self)
            return self._keys[key]
        else:
            raise KeyError()

    def keys(self):
        return list(allowed_types)

class RouteMasters():
    """
    Route masters by transport type
    """
    def __init__(self, type, city):
        self.__name__ = type # Name is also type
        self.__parent__ = city

    @_keyerror_if_none
    def __getitem__(self, name):
        session = DBSession.object_session(self.__parent__)
        return session.query(RouteMaster).filter_by(type=self.__name__,
            city=self.__parent__).first()

class RouteMaster(Base, UserDict.DictMixin):
    __tablename__ = 'route_masters'
    __table_args__ = (UniqueConstraint('city_id', 'type', 'ref'),)

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    osm_relation_id = Column(BigInteger, nullable=True)
    type = Column(String(16))
    ref = Column(String(16))
    name = Column(String)

    routes = relationship("Route")

    def keys(self):
        return range(1, len(self.routes) + 1)

    @property
    def __parent__(self):
        return self.city[self.type]

    @property
    def __name__(self):
        return self.name

    @property
    def status(self):
        return max((route.status for route in self.itervalues()),
                   key = lambda x: error_levels[x]) or "empty"

    def __getitem__(self, item):
        try:
            i = int(item)
            route = self.routes[i-1]
        except (IndexError, ValueError):
            raise KeyError()

        route._name = str(i)
        return route

    @property
    def manual_status(self):
        ms = "checked"
        for route in self.itervalues():
            if route.manual_status == "unknown":
                ms = "unknown"
            elif route.manual_status == "error":
                return "error"
        return ms

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    route_master_id = Column(Integer, ForeignKey("route_masters.id"))
    osm_relation_id = Column(BigInteger, nullable=True)
    type = Column(String)
    ref = Column(String(16))
    name = Column(String)

    status = Column(String(8), default="empty")
    # empty, vintage, notice, warning, error
    manual_status = Column(String(8), default="unknown")
    # unknown, checked, error
    relation_not_found = Column(Boolean, default=False)

    stops = Column(Text, nullable=True)

    @property
    def __name__(self):
        if not getattr(self, "_name", None):
            i = 0
            for r in self.route_master.routes:
                i += 1
                if r.id == self.id:
                    self._name = str(i)
                    break

        return self._name

    @property
    def __parent__(self):
        return self.route_master

def get_root(request=None):
    global _root_ptwatch
    if not _root_ptwatch:
        _root_ptwatch = PTWatch()
    return _root_ptwatch

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        transaction.begin()
        session = DBSession()
        city = City()
        city.name = "Yoshkar-Ola"
        city.country = "Russia"
        city.urlname = "Yoshkar-Ola"
        session.add(city)
        transaction.commit()
    except IntegrityError:
        # already created
        transaction.abort()
