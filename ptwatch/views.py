from pyramid.view import view_config
from ptwatch.models import PTWatch, City, Route

@view_config(context=PTWatch, renderer='ptwatch:templates/root.pt')
def root_view(context, request):
	return {}

@view_config(context=City, renderer='ptwatch:templates/city.pt')
def city_view(context, request):
	return dict(city=context)

@view_config(context=Route, renderer='ptwatch:templates/route.pt')
def route_view(context, request):
    return dict(route=context)
