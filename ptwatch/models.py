import transaction
from sqlalchemy import Column, Boolean, Integer, BigInteger, String, Text
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from zope.sqlalchemy import ZopeTransactionExtension

allowed_types = ['bus', 'trolleybus', 'share_taxi', 'tram']

error_levels = dict(ok=0, notice=1, warning=2, error=3, empty=4)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
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

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    urlname = Column(String)

    @property
    def __name__(self):
        return self.urlname

    @property
    def __parent__(self):
        return get_root()['cities']

    def __getitem__(self, key):
        if key in allowed_types:
            if getattr(self, "route_masters", None):
                self.route_masters = {}
                if not self.route_masters.has_key(key):
                    self.route_masters[key] = RouteMasters(key, self)
            return self.route_masters[key]
        else:
            raise KeyError()

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
            city=self.__parent__.id).first()

class RouteMaster(Base):
    __tablename__ = 'route_masters'
    __table_args__ = (UniqueConstraint('city', 'type', 'ref'),)

    id = Column(Integer, primary_key=True)
    city = Column(Integer, ForeignKey("cities.id"))
    osm_relation_id = Column(BigInteger, nullable=True)
    type = Column(String(16))
    ref = Column(String(16))
    name = Column(String)

    routes = relationship("Route")

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
            route = self.routes[i]
        except (IndexError, ValueError):
            raise KeyError()

        route.__parent__ = self
        route.__name__ = str(i)
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
    route_master = Column(Integer, ForeignKey("route_masters.id"))
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
        i = 0
        for r in self.route_master.routes:
            i += 1
            if r.id == self.id:
                return str(i)

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
    #try:
    #    transaction.begin()
    #    session = DBSession()
    #    page = Page('FrontPage', 'This is the front page')
    #    session.add(page)
    #    transaction.commit()
    #except IntegrityError:
    #    # already created
    #    transaction.abort()
