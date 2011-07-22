from django.contrib import admin
from reversion.admin import VersionAdmin
from models import RouteMaster, Route, RouteOsmStop, OsmStop, ListedStop

class RouteMasterAdmin(VersionAdmin):
    pass

class RouteAdmin(VersionAdmin):
    pass

admin.site.register(RouteMaster, RouteMasterAdmin)
admin.site.register(Route, RouteAdmin)
