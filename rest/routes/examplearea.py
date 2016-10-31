# Standard Library imports
from __future__ import print_function

# Package imports

# Local imports
from rest import settings
from rest.controllers import examplearea as controller
from rest.utilities.routebuilder import RouteBuilder


route_builder = RouteBuilder('ExampleArea')


@settings.app.route(route_builder.build_route('ExampleEntity'), ['GET'])
def exampleentity_get(offset=0, limit=10, *args, **kwargs):
    return controller.exampleentity.get(offset, limit)
