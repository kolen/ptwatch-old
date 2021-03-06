import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'repoze.retry',
    'WebError',
    'psycopg2',
    'DBUtils',
    'zope.sqlalchemy',
    'colander',
    'deform',
    ]

setup(name='ptwatch',
      version='0.0',
      description='ptwatch',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="ptwatch",
      entry_points = """\
      [paste.app_factory]
      main = ptwatch:main
      """,
      paster_plugins=['pyramid'],
      )
