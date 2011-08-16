import psycopg2
from DBUtils.PooledDB import PooledDB
from pyramid.config import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from ptwatch.models import get_root
from sqlalchemy import engine_from_config
from ptwatch.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

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

    config.add_subscriber('ptwatch.subscribers.add_base_template',
                            'pyramid.events.BeforeRender')

    config.add_static_view('static_deform', 'deform:static')

    return config.make_wsgi_app()
