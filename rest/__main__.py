# Standard Library imports
from __future__ import print_function
from time import sleep
from traceback import format_exc

# Package imports
from bottle import Bottle, BaseRequest

# Local imports
from rest import settings
from rest.plugins.bugsnagnotifier import BugsnagNotifier
from rest.plugins.requesthandler import RequestHandler
from rest.plugins.responsehandler import ResponseHandler


def initialize_bottle_app():
    settings.app = Bottle()
    from rest import hooks
    from rest import routes
    settings.app.install(BugsnagNotifier())
    # settings.app.install(plugins.DatabaseSession())
    settings.app.install(RequestHandler())
    settings.app.install(ResponseHandler())

    if __name__ == '__main__':
        # Development mode- launch internal WSGI server
        return settings.app.run(host='0.0.0.0', port=8080)
    else:
        # Deployment mode- rely on external WSGI server
        return settings.app

try:
    BaseRequest.MEMFILE_MAX = 1024 * 100000
    initialize_bottle_app()

except KeyboardInterrupt:
    # Interrupt Requested: exit
    exit()

except Exception as e:
    # Init Exception: wait and try again
    print('------------------')
    print('Unable to init app')
    print(format_exc())
    print('------------------')
    print('Retry in 5 seconds')
    sleep(5)
    initialize_bottle_app()
