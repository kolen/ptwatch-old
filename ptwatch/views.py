import re
import colander
import deform
import transaction
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from ptwatch.models import PTWatch, City, Route, RouteMaster, RouteMasters
from ptwatch.models import allowed_types

@view_config(context=PTWatch, renderer='ptwatch:templates/root.pt')
def root_view(context, request):
    return {}

@view_config(context=City, renderer='ptwatch:templates/city.pt')
def city_view(context, request):
    route_master_add_url = resource_url(context, request,
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

    form_schema = Schema()
    form = deform.Form(form_schema, buttons=('submit',))
    form['variants'].widget = deform.widget.SequenceWidget(min_len=1)

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            struct = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e.render())

        cleaned_ref = re.sub("[^a-zA-Z0-9]", "", struct['ref'])
        while context.route_masters.has_key(cleaned_ref):
            try:
                cleaned_ref_base, cleaned_ref_num = cleaned_ref.split("_")
            except ValueError:
                cleaned_ref_base, cleaned_ref_num = cleaned_ref, "0"
            cleaned_ref_num = str(int(cleaned_ref_num)+1)
            cleaned_ref = "%s_%s" % (cleaned_ref_base, cleaned_ref_num)

        master = RouteMaster(context.route_masters)
        master.__name__ = cleaned_ref

        master.ref = struct['ref']
        master.type = struct['type']
        master.name = struct['name']
        master.osm_relation_id = struct['osm_relation_id']

        for v_s in struct['variants']:
            variant = master.new()
            variant.name = v_s['name']
            variant.osm_relation_id = v_s['osm_relation_id']
            variant.stops = v_s['stops']

        context.route_masters[cleaned_ref] = master

        transaction.commit()

        return HTTPFound(location=resource_url(context, request))
    else:
        return dict(form=form.render())
