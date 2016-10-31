# Standard Library imports
from __future__ import print_function
from datetime import datetime

# Package imports
from bottle import response as Response

# Local imports
from rest import settings
from rest.plugins.baseplugin import BasePlugin
from rest.utilities.serializer import Serializer


class ResponseHandler(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, enforce_distinct=True)

    def apply(self, route, context):
        def wrapper(*args, **kwargs):
            results, count = route(*args, **kwargs)

            serializer = Serializer(kwargs['return_format'].format, Response, results, count, callback=kwargs.get('callback'))
            content = serializer.serialize()

            if isinstance(content, basestring) and settings.return_stack_trace:
                timestamp = kwargs.get('__timestamp__')
                millis = round((datetime.now() - timestamp).total_seconds() * 1000, 3) if timestamp else 0
                content = content % {'millis': millis}

            if isinstance(content, basestring):
                Response.content_length = len(content)
            return content

        return wrapper
