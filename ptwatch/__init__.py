import psycopg2
from DBUtils.PooledDB import PooledDB
from pyramid.config import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from ptwatch.models import appmaker

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    zodb_uri = settings.get('zodb_uri', False)
    if zodb_uri is False:
        raise ValueError("No 'zodb_uri' in application configuration.")

    finder = PersistentApplicationFinder(zodb_uri, appmaker)
    def get_root(request):
        return finder(request.environ)
    config = Configurator(root_factory=get_root, settings=settings)
    config.add_static_view('static', 'ptwatch:static')
    config.scan('ptwatch')

    config.registry.osm_db_pool = PooledDB(psycopg2,
        database=settings.get('osm_db_database', None),
        user=settings.get('osm_db_user', None),
        password=settings.get('osm_db_password', None),
        host=settings.get('osm_db_host', None),
    )
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

    return config.make_wsgi_app()
