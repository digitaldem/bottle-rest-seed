# Standard Library imports
from __future__ import print_function

# Package imports
from ujson import dumps

# Local imports


def serialize(results, sort=False):
    return dumps(results)
