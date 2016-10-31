# Standard Library imports
from __future__ import print_function
from os import path
from socket import gethostname, gethostbyname, gaierror

# Package imports

# Local imports


# Application variable for decorator access
app = None

# Global settings
bugsnag_key = ''
crossdomains = [{'domain': 'www.google.com', 'secure': True}]

# Environment based settings
hostname = gethostname().upper()
try:
    hostip = gethostbyname(hostname)
except gaierror:
    hostip = gethostbyname(hostname + '.local')

if hostname.startswith('P-'):
    # PROD
    environment = 'Production'
    enable_error_notification = True
    return_stack_trace = False
    database_uri = 'postgresql://localhost:5432/rest'
elif hostname.startswith('Q-'):
    # QA
    environment = 'QA'
    enable_error_notification = True
    return_stack_trace = True
    database_uri = 'postgresql://localhost:5432/rest_qa'
elif hostname.startswith('D-'):
    # DEV
    environment = 'Development'
    enable_error_notification = False
    return_stack_trace = True
    database_uri = 'postgresql://localhost:5432/rest_dev'
else:
    # LOCAL
    environment = 'Local Development'
    enable_error_notification = False
    return_stack_trace = True
    database_uri = 'postgresql://localhost:5432/rest_dev'

print('='*34)
print('=  Running in %s  =' % environment.ljust(17))
print('='*34)
