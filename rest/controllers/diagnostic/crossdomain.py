# Standard Library imports
from __future__ import print_function

# Package imports
from newrelic.agent import set_transaction_name

# Local imports
from rest import settings
from rest.utilities.returnformat import ReturnFormat


def get(return_format):
    set_transaction_name('rest.diagnostics.crossdomain:get')

    if return_format != ReturnFormat.Xml:
        raise Exception(404, 'Not found.')

    domains = [{'@domain': x.get('domain'), '@secure': 'true' if x.get('secure') else 'false'} for x in settings.crossdomains]
    output = {'cross-domain-policy': {'site-control': {'@permitted-cross-domain-policies': 'all'}, 'allow-access-from': domains}}

    return output, 0
