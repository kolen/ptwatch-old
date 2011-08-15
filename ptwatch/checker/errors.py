
import re
import sys
import inspect

class ErrorMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ErrorMetaclass, cls).__new__(cls, name, bases, attrs)
        errname = re.sub(r"(?<=[a-z])(?=[A-Z0-9])", "_", name).upper()
        new_class.name = errname
        return new_class

class Error():
    """
    Check error. Properties:
     - name: name, i.e. TOPO_BROKEN_ROUTE
     - title: descriptive title
     - severity: notice/warning/error
    """
    __metaclass__ = ErrorMetaclass

class GeneralVintage(Error):
    title = "Vintage"
    severity = "error"

class TopoNoWays(Error):
    title = "No ways"
    severity = "error"

class TopoBrokenRoute(Error):
    title = "Broken route"
    severity = "error"

    def __init__(self):
        self.broken_nodes = []

    def __repr__(self):
        return "<TopoBrokenRoute nodes=%s>" % ",".join(str(node.id) for node in self.broken_nodes)

class TopoOnewayWrongDirection(Error):
    title = "Route on one-way segments in opposite direction"
    severity = "error"

    def __init__(self):
        self.wrong_direction_ways = []

    def __repr__(self):
        return "<TopoBrokenRoute ways=%s>" % ",".join(str(node.id) for node in self.wrong_direction_ways)

class TopoStopsOutsideRoute(Error):
    title = "Stops outside route"
    severity = "error"

    def __init__(self):
        self.stops = []

class TopoWrongStopsOrder(Error):
    title = "Wrong stops order"
    severity = "error"

class TypeNoPlatformForStop(Error):
    title = "Stop have no platform"
    severity = "error"

class TypeExtraPlatformForStop(Error):
    title = "Extra platform"
    severity = "error"

class TypeWrongSorting(Error):
    title = "Wrong sorting"
    severity = "error"

class TypeWrongRole(Error):
    title = "Wrong role"
    severity = "error"

class TypeWrongObject(Error):
    title = "Wrong object"
    severity = "error"

    def __init__(self):
        self.objects = []

errors = dict((cls.name, cls)
    for clsname, cls in inspect.getmembers(sys.modules[__name__],
        lambda x: inspect.isclass(x) and issubclass(x, Error) and x != Error)
    )
