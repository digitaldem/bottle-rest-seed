# Standard Library imports
from __future__ import print_function
from datetime import datetime
from os import path

# Package imports
from bottle import request as Request, response as Response

# Local imports
from rest import settings
from rest.utilities.returnformat import ReturnFormat
from rest.utilities.serializer import Serializer


def http_500(exception, *args, **kwargs):
    timestamp = kwargs.get('__timestamp__', datetime.now())
    return_format = kwargs.get('return_format', ReturnFormat(''))
    callback = kwargs.get('callback', 'callback')
    serializer = Serializer(return_format.format, Response, exception=exception, callback=callback)
    content = serializer.serialize()

    if settings.return_stack_trace:
        millis = round((datetime.now() - timestamp).total_seconds() * 1000, 3) if timestamp else 0
        content = content % {'millis': millis}

    if isinstance(content, basestring):
        Response.content_length = len(content)
    return content


def http_404(*args, **kwargs):
    timestamp = kwargs.get('__timestamp__', datetime.now())
    return_format = ReturnFormat(path.splitext(Request.fullpath)[1].strip('.').lower())
    callback = kwargs.get('callback', 'callback')
    if return_format.format:
        serializer = Serializer(return_format.format, Response, exception='Not Found.', callback=callback)
    else:
        serializer = Serializer(ReturnFormat('html').format, Response, results='<h1>Error: 404 Not Found</h1>')
    content = serializer.serialize()

    if settings.return_stack_trace:
        millis = round((datetime.now() - timestamp).total_seconds() * 1000, 3) if timestamp else 0
        content = content % {'millis': millis}

    if isinstance(content, basestring):
        Response.content_length = len(content)
    return content


settings.app.error_handler = {
    500: http_500,
    404: http_404
}
