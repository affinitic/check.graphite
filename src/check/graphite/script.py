# encoding: utf-8
"""
check.graphite

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

from StringIO import StringIO
import argparse
import gzip
import json
import operator
import requests
import sys


def check_graphite():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str,
                        help='Graphite host e.g. http://host.com/render')
    parser.add_argument('metric', type=str)
    parser.add_argument('-n', '--name', type=str, default=None)
    parser.add_argument('-t', '--timeframe', type=str, default='30seconds')
    parser.add_argument('-w', '--warning', type=float, default=100.0)
    parser.add_argument('-c', '--critical', type=float, default=200.0)

    cls = CheckGraphite(**parser.parse_args().__dict__)
    status, message = cls.process()
    print message
    sys.exit(status)


class CheckGraphite(object):

    status_match = {
        'critical': 2,
        'warning': 1,
    }

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, '%s' % k, v)
        self.status = ['critical', 'warning']
        self.op = operator.ge
        if self.critical < self.warning:
            self.op = operator.le
            self.status.reverse()

    def process(self):
        try:
            result = json.loads(requests.get(self.url).content)
        except ValueError:
            result = None
        if not result:
            return 3, 'UNKNOWN - no data'
        if self.name is None:
            self.name = result[0].get('target')
        return self.process_result(result[0])

    def process_result(self, result):
        if len(result.get('datapoints', [])) == 0:
            return 3, 'UNKNOWN - no valid datapoints'
        values = [d[0] for d in result.get('datapoints') if d[0]]
        avg = values and self.get_average(values) or 0
        for status in self.status:
            if self.op(avg, getattr(self, status)):
                return (self.status_match.get(status),
                        '%s - %s=%s' % (status.upper(), self.name, avg))
        return 0, 'OK - %s=%s' % (self.name, avg)

    @staticmethod
    def handle_gzip_content(content):
        buffer = StringIO(content)
        f = gzip.GzipFile(fileobj=buffer)
        return f.read()

    @property
    def url(self):
        url_format = '%(host)s?target=%(metric)s&from=-%(timeframe)s&format=json'
        return url_format % self.__dict__

    @staticmethod
    def get_average(values):
        return sum(values) / len(values)
