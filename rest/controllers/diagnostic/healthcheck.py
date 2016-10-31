# Standard Library imports
from __future__ import print_function
from os import path

# Package imports
from newrelic.agent import set_transaction_name

# Local imports
from rest import settings
from rest.utilities.returnformat import ReturnFormat


def get(return_format):
    set_transaction_name('rest.diagnostic.healthcheck:get')
    status = _check_online_file()
    bugsnag = settings.enable_error_notification

    if return_format.format == ReturnFormat.Html:
        output = _build_response_html(settings.hostname,
                                      settings.hostip,
                                      _get_status_message(status),
                                      _get_bugsnag_message(bugsnag),
                                      settings.environment)
    else:
        output = [{'hostName': settings.hostname,
                   'hostIP': settings.hostip,
                   'environment': settings.environment,
                   'status': 'ONLINE' if status else 'OFFLINE',
                   'bugsnag': 'ENABLED' if bugsnag else 'DISABLED'}]

    return output, 0


def _get_status_message(is_online):
    if is_online:
        return _get_message('#41A317', 'ONLINE')
    else:
        return _get_message('#F62217', 'OFFLINE')


def _get_bugsnag_message(is_enabled):
    if is_enabled:
        return _get_message('#41A317', 'enabled')
    else:
        return _get_message('#F62217', 'disabled')


def _check_online_file():
    return path.isfile(path.abspath(path.join(path.dirname(path.realpath(__file__)), '..', '..', 'online')))


def _get_message(color, msg):
    return '<font color="' + color + '"><b>' + msg + '</b></font>'


def _build_response_html(hostname, hostip, status, bugsnag, env):
    return """
    <html>
        <head>
        <title>Diagnostic - Test</title>
        </head>
        <body bgcolor="#FFFFFF">
            <h2>Hello from</h2>
            <h2>%s</h2>
            <h3>(%s)</h3>
            <font color="#5C5C5C">
            <br/>
            Traffic is %s
            <br/>
            <br/>
            Bugsnag is %s
            <br/>
            <br/>
            In the <font color="#000000"><b>%s</b></font> environment
            <br/>
            <br/>
            Response took %s milliseconds to generate
            </font>
        </body>
    </html>\n\n""" % (hostname, hostip, status, bugsnag, env, '%(millis)0.3f')
