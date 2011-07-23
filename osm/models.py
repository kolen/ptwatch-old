# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

#class SpatialRefSys(models.Model):
#    srid = models.IntegerField(primary_key=True)
#    auth_name = models.CharField(max_length=256)
#    auth_srid = models.IntegerField()
#    srtext = models.CharField(max_length=2048)
#    proj4text = models.CharField(max_length=2048)
#    class Meta:
#        db_table = u'spatial_ref_sys'
#
#class GeometryColumns(models.Model):
#    f_table_catalog = models.CharField(max_length=256)
#    f_table_schema = models.CharField(max_length=256)
#    f_table_name = models.CharField(max_length=256)
#    f_geometry_column = models.CharField(max_length=256)
#    coord_dimension = models.IntegerField()
#    srid = models.IntegerField()
#    type = models.CharField(max_length=30)
#    class Meta:
#        db_table = u'geometry_columns'
#
#class GeographyColumns(models.Model):
#    f_table_catalog = models.TextField() # This field type is a guess.
#    f_table_schema = models.TextField() # This field type is a guess.
#    f_table_name = models.TextField() # This field type is a guess.
#    f_geography_column = models.TextField() # This field type is a guess.
#    coord_dimension = models.IntegerField()
#    srid = models.IntegerField()
#    type = models.TextField()
#    class Meta:
#        db_table = u'geography_columns'
#
#class SchemaInfo(models.Model):
#    version = models.IntegerField(primary_key=True)
#    class Meta:
#        db_table = u'schema_info'

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'users'

class Node(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    user = models.ForeignKey(User)
    tstamp = models.DateTimeField()
    changeset_id = models.BigIntegerField()
    geom = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'nodes'

class NodeTag(models.Model):
    node_id = models.ForeignKey(Node)
    k = models.TextField()
    v = models.TextField()
    class Meta:
        db_table = u'node_tags'

class Way(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    user = models.ForeignKey(User)
    tstamp = models.DateTimeField()
    changeset_id = models.BigIntegerField()
    class Meta:
        db_table = u'ways'

class WayNode(models.Model):
    way_id = models.ForeignKey(Way)
    node_id = models.ForeignKey(Node)
    sequence_id = models.IntegerField()
    class Meta:
        db_table = u'way_nodes'

class WayTag(models.Model):
    way_id = models.ForeignKey(Way)
    k = models.TextField()
    v = models.TextField()
    class Meta:
        db_table = u'way_tags'

class Relation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.IntegerField()
    user = models.ForeignKey(User)
    tstamp = models.DateTimeField()
    changeset_id = models.BigIntegerField()
    class Meta:
        db_table = u'relations'

class RelationMember(models.Model):
    relation_id = models.BigIntegerField()
    member_id = models.BigIntegerField()
    member_type = models.TextField() # This field type is a guess.
    member_role = models.TextField()
    sequence_id = models.IntegerField()
    class Meta:
        db_table = u'relation_members'

class RelationTag(models.Model):
    relation_id = models.ForeignKey(Relation, related_name='tags')
    k = models.TextField()
    v = models.TextField()
    class Meta:
        db_table = u'relation_tags'

