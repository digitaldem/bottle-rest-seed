# Standard Library imports
from __future__ import print_function

# Package imports
from bottle import response as Response

# Local imports
from rest.settings import app


@app.hook('after_request')
def enable_cors():
    Response['access-control-allow-origin'] = '*'
    Response['access-control-allow-methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    Response['access-control-allow-headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
