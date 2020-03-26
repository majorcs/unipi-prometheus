#!/usr/bin/python2

import json
import logging
import sys
import time
import urllib2
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class UniPiCollector(object):
  def collect(self):
    metric = GaugeMetricFamily(
        'unipi_01',
        'Unipi cucc',
        labels=["circuit", "dev"])

    try:
        result = json.load(urllib2.urlopen("http://192.168.88.32:8080/rest/all", timeout=10))
        logging.info("Result fetched")
        self.result = result
    except:
        logging.info("Result fetch failed, use old values")
        if not hasattr(self, 'result'):
            self.result = []
        result = self.result
            
    logging.debug("Result: %s" % (self.result))

    for obj in result:
        metric.add_metric([obj.get('circuit'), obj.get('dev')], obj.get('value', 0))

    yield metric

if __name__ == "__main__":
  logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
  logging.info("Starting main loop")
  REGISTRY.register(UniPiCollector())
  start_http_server(9118)
  while True: time.sleep(1)
