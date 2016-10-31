# Standard Library imports
from __future__ import print_function

# Package imports
from bottle import request as Request

# Local imports
from rest import settings
from rest.plugins.baseplugin import BasePlugin
from rest.utilities.string import sanitize_quotes


class RequestHandler(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, enforce_distinct=True)

    def apply(self, response_handler, context):
        def wrapper(*args, **kwargs):
            # Include the individual request data in the kwargs for processing
            request_params = RequestHandler._get_request_params(Request)
            RequestHandler._add_request_params_to_kwargs(kwargs, request_params)

            # Include the raw request data payload in the kwargs for debuging and logging
            kwargs['__request__'] = {'resource': kwargs.get('entity', ''),
                                     'url': Request.url,
                                     'headers': dict(Request.headers),
                                     'params': dict(Request.params)}

            return response_handler(*args, **kwargs)

        return wrapper

    @staticmethod
    def _get_request_params(request):
        return {key.lower(): request.params[key] for key in request.params}

    @staticmethod
    def _add_request_params_to_kwargs(kwargs, request_params):
        for key in request_params:
            if (key not in kwargs or not kwargs[key]) and RequestHandler._is_valid_value(request_params[key]):
                kwargs[key] = sanitize_quotes(request_params[key].strip())

    @staticmethod
    def _is_valid_value(val):
        return val.lower().strip() not in ['', 'null', 'undefined']
