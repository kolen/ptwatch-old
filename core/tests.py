"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from tempfile import mkdtemp
import logging
import re
import os.path

from django.test import TestCase
from django.conf import settings
from django.db import connections, transaction


class CheckerTest(TestCase):
#    def setUp(self):
#        script = open("testdata/pgsimple_schema_0.6.sql").read()
#        script += open("testdata/pgsimple_load_0.6.sql").read()
#        path = os.path.abspath("testdata/import_data")
#        script = re.sub("(?<=FROM ')(?=[a-z_]+\.txt')", path, script)
#        script = script.replace(r"\copy", "copy")
#        c = connections['osm'].cursor()
#        for statement in script.split(';'):
#            c.execute(statement)

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
