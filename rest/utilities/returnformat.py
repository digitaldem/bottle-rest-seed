# Standard Library imports
from __future__ import print_function

# Package imports

# Local imports


class ReturnFormat(object):
    Json = 'json'
    Jsonp = 'jsonp'
    Html = 'html'
    Xml = 'xml'
    Csv = 'csv'
    Xlsx = 'xlsx'

    def __init__(self, fmt):
        self.format = next((val for val in ReturnFormat.__dict__.values() if isinstance(val, basestring) and fmt.lower() == val.lower()), '')
