# Standard Library imports
from __future__ import print_function

# Package imports

# Local imports
from rest import settings
from rest.controllers import diagnostic as controller
from rest.utilities.routebuilder import RouteBuilder


route_builder = RouteBuilder()


@settings.app.route(route_builder.build_route('HealthCheck'), ['GET'])
def healthcheck_get(return_format, *args, **kwargs):
    return controller.healthcheck.get(return_format)


@settings.app.route(route_builder.build_route('CrossDomain'), ['GET'])
def crossdomain_get(return_format, *args, **kwargs):
    return controller.crossdomain.get(return_format)
