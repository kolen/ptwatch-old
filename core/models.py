from django.db import models
import reversion

class RouteMaster(models.Model):
    ref = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    osm_ref = models.CharField(max_length=64)
    osm_name = models.CharField(max_length=128)
    osm_operator = models.CharField(max_length=255)
    osm_colour = models.CharField(max_length=32)
    osm_relation_id = models.BigIntegerField(null=True)

reversion.register(RouteMaster, fields=["ref", "name"])

class RouteOsmStop(models.Model):
    order = models.PositiveSmallIntegerField()
    route = models.ForeignKey("Route")
    osm_stop = models.ForeignKey("OsmStop")
    matched_listed_stop = models.ForeignKey("ListedStop")

class Route(models.Model):
    ref = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    osm_ref = models.CharField(max_length=64)
    osm_name = models.CharField(max_length=128)
    osm_operator = models.CharField(max_length=255) 
    osm_colour = models.CharField(max_length=32)
    osm_relation_id = models.BigIntegerField(null=True)
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
    name = models.CharField(max_length=128)
    
reversion.register(ListedStop)
