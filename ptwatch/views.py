import re
import colander
import deform
import transaction
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from ptwatch.models import PTWatch, City, Route, RouteMaster, RouteMasters
from ptwatch.models import allowed_types, DBSession, IntegrityError

@view_config(context=PTWatch, renderer='ptwatch:templates/root.pt')
def root_view(context, request):
    return {}

@view_config(context=City, renderer='ptwatch:templates/city.pt')
def city_view(context, request):
    session = DBSession()
    rms = session.query(RouteMaster).filter_by(city=context).all()

    route_masters_by_transport = [
        (type, [rm for rm in rms if rm.type == type])
        for type in allowed_types
    ]
    return dict(city=context, route_masters_by_transport=route_masters_by_transport)

@view_config(context=RouteMaster, renderer='ptwatch:templates/route_master.pt')
def route_master_view(context, request):
    return dict(route_master=context)

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

    def validator(form, value):
        session = DBSession()
        if session.query(RouteMaster).filter_by(ref=value['ref'],
                city=context, type=value['type']).count() != 0:
            t = 'Route with this ref and type already exists'
            exc = colander.Invalid(form, t)
            exc['ref'] = t
            raise exc

    form_schema = Schema(validator=validator)
    form = deform.Form(form_schema, buttons=('submit',))
    form['variants'].widget = deform.widget.SequenceWidget(min_len=1)

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            struct = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e.render())

        session = DBSession()

        master = RouteMaster()
        master.city = context
        master.ref = struct['ref']
        master.type = struct['type']
        master.name = struct['name']
        master.osm_relation_id = struct['osm_relation_id']

        for v_s in struct['variants']:
            variant = Route()
            variant.name = v_s['name']
            variant.osm_relation_id = v_s['osm_relation_id']
            variant.stops = v_s['stops']
            master.routes.append(variant)

        context.route_masters.append(master)

        session.flush()
        transaction.commit()

        return HTTPFound(location=resource_url(context, request))
    else:
        return dict(form=form.render())
