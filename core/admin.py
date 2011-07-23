from django.contrib import admin
from reversion.admin import VersionAdmin
from models import RouteMaster, Route, RouteOsmStop, OsmStop

class RouteMasterAdmin(VersionAdmin):
    pass

class RouteAdmin(VersionAdmin):
    pass

admin.site.register(RouteMaster, RouteMasterAdmin)
admin.site.register(Route, RouteAdmin)
#admin.site.register(ListedStop, ListedStopInline)
