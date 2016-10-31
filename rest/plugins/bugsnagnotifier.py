# Standard Library imports
from __future__ import print_function
from datetime import datetime
from traceback import format_exc

# Package imports
from bottle import request as Request
from bugsnag import configure, configure_request, clear_request_config, notify

# Local imports
from rest import settings
from rest.plugins.baseplugin import BasePlugin
from rest.utilities.returnformat import ReturnFormat


class BugsnagNotifier(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, enforce_distinct=True)
        configure(api_key=settings.bugsnag_key, release_stage=settings.environment)

    def apply(self, request_handler, context):
        def wrapper(*args, **kwargs):
            try:
                kwargs['__timestamp__'] = datetime.now()
                kwargs['return_format'] = ReturnFormat(kwargs.get('return_format'))

                return request_handler(*args, **kwargs)

            except KeyboardInterrupt:
                exit()

            except Exception as ex:
                status, message = ex.args if len(ex.args) == 2 else (None, None)

                # Handled exception
                if isinstance(status, int) and 100 <= status <= 999:
                    if status in settings.app.error_handler:
                        # Call appropriate error handler based on status code
                        return settings.app.error_handler[status](message, *args, **kwargs)

                    # Unknown status code, alert and then just let the default 500 status handler
                    if settings.enable_error_notification:
                        self._notify_bugsnag('No handler defined for HTTP %d status code.' % status)
                    return settings.app.error_handler[500](message, *args, **kwargs)

                # Unhandled exception, alert and then just let the default 500 status handler
                if settings.enable_error_notification:
                    self._notify_bugsnag(ex)

                exc = format_exc()
                print('-------------Exception')
                print(exc)
                print('-------------')
                return settings.app.error_handler[500](exc if settings.return_stack_trace else 'Unknown error.', *args, **kwargs)

        return wrapper

    def _notify_bugsnag(self, exception):
        try:
            configure_request(context='%s %s' % (Request.method, Request.environ.get('PATH_INFO', '')),
                              user_id=Request.remote_addr,
                              request_data={'url': Request.url,
                                            'headers': dict(Request.headers),
                                            'cookies': dict(Request.cookies),
                                            'params': dict(Request.params)},
                              environment_data=dict(Request.environ))
            notify(exception)
            clear_request_config()
        except:
            pass
