import colander
import deform
from pyramid.view import view_config
from pyramid.url import resource_url
from ptwatch.models import PTWatch, City, Route, RouteMaster, RouteMasters
from ptwatch.models import allowed_types

@view_config(context=PTWatch, renderer='ptwatch:templates/root.pt')
def root_view(context, request):
    return {}

@view_config(context=City, renderer='ptwatch:templates/city.pt')
def city_view(context, request):
    route_master_add_url = resource_url(context.route_masters, request,
        'add_route_master')
    return dict(city=context, route_master_add_url=route_master_add_url)

@view_config(context=Route, renderer='ptwatch:templates/route.pt')
def route_view(context, request):
    return dict(route=context)

@view_config(name='add_route_master', context=City,
    renderer='ptwatch:templates/route_master_add.pt')
def route_add(context, request):
    class RouteVariantSchema(colander.Schema):
        name = colander.SchemaNode(
            colander.String(),
            description="Variant name",
            missing=u'')
        osm_relation_id = colander.SchemaNode(
            colander.Int(),
            title="Openstreetmap Relation ID (type=route)",
            description="Openstreetmap relation ID of this route variant, if "
                "it exists in openstreetmap. Relation should have "
                "type=route key.",
            missing=None)
        stops = colander.SchemaNode(
            colander.String(),
            description="Stops, one stop name per line",
            missing=u'',
            widget=deform.widget.TextAreaWidget(rows=10, cols=60))

    class VariantsSequence(colander.SequenceSchema):
        variant = RouteVariantSchema()

    class Schema(colander.Schema):
        type = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(
                values=[('', '- Select -')] + [(v, v) for v in allowed_types]))
        ref = colander.SchemaNode(
            colander.String(),
            description="Route ref, i.e. '22'")
        name = colander.SchemaNode(
            colander.String(),
            description="Route name",
            missing=u'')
        osm_relation_id = colander.SchemaNode(
            colander.Int(),
            title="Openstreetmap Relation ID (type=route_master)",
            description="Openstreetmap relation ID of this route variant, if "
                "it exists in openstreetmap. Relation should have "
                "type=route key.",
            missing=None)
        variants = VariantsSequence()

    schema = Schema()
    form = deform.Form(schema, buttons=('submit',))
    form['variants'].widget = deform.widget.SequenceWidget(min_len=1)

    return dict(form=form.render())
