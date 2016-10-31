# Standard Library imports
from __future__ import print_function

# Package imports

# Local imports
from rest import settings
from rest.serializers import csv, excel, html, json, xml


class Serializer(object):
    def __init__(self, serialize_format, response, results=[], count=0, exception=None, callback='callback'):
        self.format = serialize_format
        self.response = response
        self.results = results
        self.count = count
        self.exception = exception
        self.callback = callback

    def serialize(self):
        try:
            generator = getattr(self, 'generate_' + self.format)
            return generator()
        except AttributeError:
            self.response.content_type = 'text/html'
            return 'Unknown format requested'

    def generate_json(self):
        self.response.content_type = 'application/json'

        self._build_results_dict()
        return json.serialize(self.results)

    def generate_jsonp(self):
        self.response.content_type = 'text/plain'

        self._build_results_dict()
        return '%s(%s)' % (self.callback, json.serialize(self.results))

    def generate_html(self):
        self.response.content_type = 'text/html'

        if isinstance(self.results, basestring):
            return self.results
        self._build_results_dict()
        return html.serialize(self.results)

    def generate_xml(self):
        self.response.content_type = 'text/xml'

        if not isinstance(self.results, dict):
            self._build_results_dict()
        return xml.serialize(self.results, defaulttag=None)

    def generate_csv(self):
        self.response.content_type = 'application/force-download;'
        self.response.headers['Content-Disposition'] = 'attachment; filename="export.csv"'

        return csv.serialize(self.results)

    def generate_xlsx(self):
        self.response.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.response.headers['Content-Disposition'] = 'attachment; filename="export.xlsx"'

        return excel.serialize(self.results)

    def _build_results_dict(self):
        self.results = {'results': self.results,
                        'totalCount': self.count,
                        'exception': self.exception}

        if settings.return_stack_trace:
            self.results['host'] = '%s (%s)' % (settings.hostname, settings.hostip)
            self.results['millis'] = '%(millis)0.3f'
