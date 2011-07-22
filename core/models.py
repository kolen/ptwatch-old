from django.db import models
import reversion

class RouteMaster(models.Model):
    ref = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=128, blank=True)
    osm_ref = models.CharField(max_length=64, blank=True)
    osm_name = models.CharField(max_length=128, blank=True)
    osm_operator = models.CharField(max_length=255, blank=True)
    osm_colour = models.CharField(max_length=32, blank=True)
    osm_relation_id = models.BigIntegerField(null=True, blank=True)

reversion.register(RouteMaster, fields=["ref", "name"])

class RouteOsmStop(models.Model):
    order = models.PositiveSmallIntegerField()
    route = models.ForeignKey("Route")
    osm_stop = models.ForeignKey("OsmStop")
    matched_listed_stop = models.ForeignKey("ListedStop")

class Route(models.Model):
    master = models.ForeignKey(RouteMaster, null=True, blank=True)
    ref = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=128, blank=True)
    osm_ref = models.CharField(max_length=64, blank=True)
    osm_name = models.CharField(max_length=128, blank=True)
    osm_operator = models.CharField(max_length=255, blank=True) 
    osm_colour = models.CharField(max_length=32, blank=True)
    osm_relation_id = models.BigIntegerField(null=True, blank=True)
    is_vintage = models.BooleanField()
    osm_stops = models.ManyToManyField("OsmStop", through="RouteOsmStop")

reversion.register(Route, fields=["ref", "name"])

class OsmStop(models.Model):
    name = models.CharField(max_length=128)
    osm_stop_id = models.BigIntegerField(null=True)
    osm_platform_id = models.BigIntegerField(null=True)

class ListedStop(models.Model):
    route = models.ForeignKey(Route)
    order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=128, blank=True)
    
reversion.register(ListedStop)
