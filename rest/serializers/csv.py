# Standard Library imports
from __future__ import print_function
from tempfile import TemporaryFile

# Package imports

# Local imports
from rest.utilities.unicodedictwriter import UnicodeDictWriter


def serialize(results):
    temp_file = TemporaryFile()
    headers = results[0].keys()
    writer = UnicodeDictWriter(temp_file, headers)
    writer.writeheader()
    writer.writerows(results)
    temp_file.seek(0)

    return temp_file
