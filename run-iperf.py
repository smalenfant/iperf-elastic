#!/usr/bin/env python
import os
import subprocess
import shlex
import json
from datetime import datetime
from elasticsearch import Elasticsearch

elastic_url = os.getenv('elastic_url', 'http://elasticsearch:9200')
iperf_host  = os.getenv('iperf_host', '127.0.0.1')
iperf_port  = os.getenv('iperf_port', '5201')

mapping = '''
{
  "mappings": {
    "doc": {
      "properties": {
        "start.timestamp.timesecs": {
          "type": "date",
          "format": "epoch_second"
        }
      }
    }
  }
}
'''

command = "iperf3 --client " + iperf_host + " --port " + iperf_port + " --json -b 100k -u -l 25 -J -i 0"
args = shlex.split(command)
print args
proc = subprocess.Popen(args,stdout=subprocess.PIPE)
(out, err) = proc.communicate()

doc = json.loads(out)
doc['hostname'] = os.environ['HOSTNAME']
doc['location'] = os.getenv('location', 'unknown')

# Ship data to Elastic Search
es = Elasticsearch(elastic_url,verify_certs=False)
index = 'latency-' + datetime.fromtimestamp(doc['start']['timestamp']['timesecs']).strftime('%Y.%m.%d')
if not es.indices.exists(index):
  es.indices.create(index, ignore=400, body=mapping)

results = es.index(index=index, doc_type="doc", body=doc)
