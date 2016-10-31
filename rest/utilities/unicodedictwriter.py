# Standard Library imports
from __future__ import print_function
from codecs import getincrementalencoder
from cStringIO import StringIO
from csv import writer

# Package imports

# Local imports


class UnicodeDictWriter(object):
    def __init__(self, f, fieldnames, dialect='excel', encoding='utf-8', **kwargs):
        self.fieldnames = fieldnames
        self.queue = StringIO()
        self.writer = writer(self.queue, dialect=dialect, **kwargs)
        self.stream = f
        self.encoder = getincrementalencoder(encoding)()

    def writeheader(self):
        self.writer.writerow(self.fieldnames)

    def writerow(self, row):
        self.writer.writerow([row[x].encode('utf-8') if hasattr(row[x], 'encode') else row[x] for x in self.fieldnames])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
