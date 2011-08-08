
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
    __metaclass__ = ErrorMetaclass

class TopoNoWays(Error):
    descr = "No ways"
    severity = "critical"

class TopoBrokenRoute(Error):
    descr = "Broken route"
    severity = "error"

class TypeNoPlatformForStop(Error):
    descr = "Stop have no platform"
    severity = "error"

class TypeWrongSorting(Error):
    descr = "Wrong sorting"
    severity = "error"

class TypeWrongRole(Error):
    descr = "Wrong role"
    severity = "error"

errors = dict((cls.name, cls)
    for clsname, cls in inspect.getmembers(sys.modules[__name__],
        lambda x: inspect.isclass(x) and issubclass(x, Error) and x != Error)
    )
