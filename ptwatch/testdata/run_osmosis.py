#!/usr/bin/env python
import os
osmosis_path = r'C:\items\osmosis-0.39\bin\osmosis.bat'
command = ('%(osmosis)s --read-xml "%(xml)s" --write-pgsimp-dump '
            'directory="%(tempdir)s"' % {
                'osmosis': osmosis_path,
                'xml': "test.osm",
                'tempdir': "./import_data",
            })
result = os.system(command)
assert(result == 0)
