# Standard Library imports
from __future__ import print_function
from numbers import Number

# Package imports

# Local imports


def serialize(results):
    return _indent_html(results)


def _indent_html(results, indent=1):
    if isinstance(results, list):
        htmls = []
        for k in results:
            htmls.append(_indent_html(k, indent+1))
        return '[<div style="margin-left: %dem">%s</div>]' % (indent, ',<br>'.join(htmls))

    if isinstance(results, dict):
        htmls = []
        for key, val in sorted(results.iteritems()):
            htmls.append('<span class="prop" style="font-weight: bold; color: #000000">%s</span>: %s' % (key, _indent_html(val, indent+1)))
        return '{<div style="margin-left: %dem">%s</div>}' % (indent, ',<br>'.join(htmls))

    if results is None:
        return '<span class="val" style="color: #FA2F00">null</span>'

    if isinstance(results, bool):
        return '<span class="val" style="color: #001FBD">%s</span>' % (str(results).lower())

    if isinstance(results, Number):
        return '<span class="val" style="color: #001FBD">%s</span>' % (results)

    if isinstance(results, str) and (results.startswith('http://') or results.startswith('https://')):
        return '<a class="val" style="color: #346A15" href="%s">%s</a>' % (results, results)

    return '<span class="val" style="color: #346A15">"%s"</span>' % (results)
