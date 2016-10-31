# Standard Library imports
from __future__ import print_function
from re import sub

# Package imports

# Local imports


standard_delimiters = ', ;'  # listed in priority order
list_notation_chars = {
    0x005B: u'',  # left square bracket
    0x005D: u'',  # right square bracket
    0x0028: u'',  # left paren
    0x0029: u'',  # right paren
    0x007B: u'',  # left curly brace
    0x007D: u'',  # right curly brace
    0x003C: u'',  # less than
    0x003E: u''   # greater than
}
artifact_chars = {
    0x0022: u'',  # quotation mark
    0x0027: u'',  # apostrophe
    0x002F: u''   # forward slash
}
quote_chars = {
    0x2018: u'\'',  # left smart quote
    0x2019: u'\'',  # right smart quote
    0x201C: u'"',   # left smart double quote
    0x201D: u'"'    # right smart double quote
}


def sanitize_quotes(string):
    string = unicode(string, 'utf-8') if isinstance(string, str) else string
    return string.translate(quote_chars)


def delimited_str_to_int_list(string, delimiter='', clean=lambda x: x.translate(artifact_chars)):
    result = []

    if string:
        string = unicode(string, 'utf-8') if isinstance(string, str) else string
        string = string.translate(list_notation_chars)
        string = sub(r'(-)\1+', r'\1', string)

        if not delimiter:
            delimiter = _get_delimiter(string)

        try:
            result = [int(clean(s)) for s in string.split(delimiter) if s] if delimiter else [int(clean(string))]

        except ValueError as ex:
            msg = 'Invalid numeric value of %s was passed.' % str(ex).split(':')[-1].strip()
            raise Exception(msg)

    return result


def delimited_str_to_str_list(string, delimiter='', clean=lambda x: x.strip()):
    result = []

    if string:
        string = unicode(string, 'utf-8') if isinstance(string, str) else string
        string = string.translate(list_notation_chars)
        if not delimiter:
            delimiter = _get_delimiter(string)

        if delimiter:
            result = [clean(s) for s in string.split(delimiter) if clean(s)]
        else:
            result = [clean(string)]

    return result


def _get_delimiter(string):
    for delimiter in standard_delimiters:
        if delimiter in string:
            return delimiter

    return ''
