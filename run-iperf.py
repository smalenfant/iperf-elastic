#!/usr/bin/env python
import os
import subprocess
import shlex
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch

elastic_url = os.getenv('elastic_url', 'http://elasticsearch:9200')
iperf_host  = os.getenv('iperf_host', '127.0.0.1')
iperf_port  = os.getenv('iperf_port', '5201')
params      = os.getenv('params','--bandwidth 1m')

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

# Connect and set mapping
es = Elasticsearch(elastic_url,verify_certs=False)
index = 'latency-' + datetime.today().strftime('%Y.%m.%d')
if not es.indices.exists(index):
  es.indices.create(index, ignore=400, body=mapping)

command = ['iperf3', '--json', '-interval', '0']

# Add Client/Target
command.append('--client')
command.append(iperf_host)

# Add port
command.append('--port')
command.append(iperf_port)

command.extend(shlex.split(params))
 
def run_iperf (command):
  print command
  #args = shlex.split(command)
  retry = 1
  while retry:
    proc = subprocess.Popen(command,stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    doc = json.loads(out)
    if 'error' in doc:
      retry = 1
      print doc['error']
      time.sleep(10)
    else:
      retry = 0

  doc['hostname'] = os.environ['HOSTNAME']
  doc['location'] = os.getenv('location', 'unknown')

  # Flatten end.streams.udp.out_of_order
  end_streams = doc['end'].pop('streams')
  
  doc['end']['sum']['out_of_order'] = end_streams[0]['udp']['out_of_order']
 
  # Remove intervals and starts.connected
  doc.pop('intervals')
  doc['start'].pop('connected')
  
  results = es.index(index=index, doc_type="doc", body=doc)
  print results

# Run once (downstream)
run_iperf(command)

# Run again (upstream)
command.append('--reverse')
run_iperf(command)
