from django.contrib import admin
from models import RouteMaster, Route, RouteOsmStop, OsmStop, ListedStop

class RouteMasterAdmin(admin.ModelAdmin):
    pass

admin.site.register(RouteMaster, RouteMasterAdmin)
