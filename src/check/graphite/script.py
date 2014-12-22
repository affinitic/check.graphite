# encoding: utf-8
"""
check.graphite

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

from StringIO import StringIO
import gzip
import json
import operator
import requests
import sys

from check.graphite.parser import ArgumentParser


def check_graphite():
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', type=str,
                        help='Graphite host e.g. http://host.com/render')
    parser.add_argument('-m', '--metrics', type=str,
                        help='metric names separate by a comma')
    parser.add_argument('-n', '--name', type=str, default='undefined')
    parser.add_argument('-t', '--timeframe', type=str, default='30seconds')
    parser.add_argument('-w', '--warning', type=float, default=100.0)
    parser.add_argument('-c', '--critical', type=float, default=200.0)

    cls = CheckGraphite(**parser.parse_args().__dict__)
    status, message = cls.process()
    print message
    sys.exit(status)


class CheckGraphite(object):

    status_match = {
        'unknown': 3,
        'critical': 2,
        'warning': 1,
        'ok': 0,
        0: 'ok',
        1: 'warning',
        2: 'critical',
        3: 'unknown',
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
        results = []
        for url in self.urls:
            results.append(self.get_result(url))
        status = sorted([r[0] for r in results], reverse=True)[0]
        info = '%s - %s - %s' % (self.status_match.get(status).upper(),
                                 self.name,
                                 ', '.join([r[1] for r in results]))
        return status, info

    def get_result(self, url):
        try:
            result = json.loads(requests.get(url).content)
        except ValueError:
            result = None
        if not result:
            return 3, 'no data'
        return self.process_result(result[0])

    def process_result(self, result):
        if len(result.get('datapoints', [])) == 0:
            return 3, 'no valid datapoints'
        values = [d[0] for d in result.get('datapoints')
                  if d[0] not in (None, '')]
        avg = values and self.get_average(values) or 0
        name = result.get('target').split('.')[-1]
        for status in self.status:
            if self.op(avg, getattr(self, status)):
                return (self.status_match.get(status),
                        '%s=%s' % (name, avg))
        return 0, '%s=%s' % (name, avg)

    @staticmethod
    def handle_gzip_content(content):
        buffer = StringIO(content)
        f = gzip.GzipFile(fileobj=buffer)
        return f.read()

    @property
    def urls(self):
        url_format = '%(host)s?target=%(metric)s&from=-%(timeframe)s&format=json'
        metrics = self.metrics.split(',')
        values = self.__dict__
        urls = []
        for metric in metrics:
            values['metric'] = metric
            urls.append(url_format % values)
        return urls

    @staticmethod
    def get_average(values):
        return sum(values) / len(values)
