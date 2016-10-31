# Standard Library imports
from __future__ import print_function

# Package imports

# Local imports


class RouteBuilder(object):
    Root = r'/'
    AlphaID = r'<id:re:(/[A-z]+)?>'
    NumericID = r'<id:re:(/[-\d]+)?>'
    AlphaNumericID = r'<id:re:(/[-\w]+)?>'
    Format = r'<return_format:re:((?i)([\w]+))>'

    def __init__(self, area=''):
        self.Area = r'<area:re:(?i)' + area + r'/?>'

    def build_route(self, entity, alpha_id=False, numeric_id=False, ):
        entity_regex = r'<entity:re:(?i)\b' + entity + r'\b>'
        if alpha_id and numeric_id:
            id_regex = self.AlphaNumericID
        elif alpha_id:
            id_regex = self.AlphaID
        elif numeric_id:
            id_regex = self.NumericID
        else:
            id_regex = ''

        return ''.join((self.Root, self.Area, entity_regex, id_regex, '.', self.Format))
