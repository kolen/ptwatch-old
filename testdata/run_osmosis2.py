#!/usr/bin/env python
import os
osmosis_path = r'C:\items\osmosis-0.39\bin\osmosis.bat'
command = ('%(osmosis)s --read-xml "%(xml)s" --write-pgsimp '
            'user="postgres" password="123" database="test_osm_small" ' % {
                'osmosis': osmosis_path,
                'xml': "test.osm",
            })
result = os.system(command)
assert(result == 0)
