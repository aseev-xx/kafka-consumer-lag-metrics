#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import ConfigParser
import time
import socket
import os

# get base json object for next
def get_json_object(url):

   try:
      obj = requests.get(url)
   except requests.exceptions.RequestException as e:
      print e
      sys.exit(1)

   return obj.json()

# get all exist clusters for url concatenate in future
def get_clusters(base_url):
   obj = get_json_object(base_url + '/api/status/clusters')
   clusters = []

   for el in obj["clusters"]["active"]:
      clusters.append(el["name"])

   return clusters
   
def prepare_graphite_metrics(base_url,graphite_prefix):

   clusters = get_clusters(base_url)

   metrics = []

   timestamp = int(time.time())

   for cluster in clusters:
      url = base_url + '/api/status/' + cluster + '/consumersSummary'   
      obj = get_json_object(url)
      consumers = obj["consumers"]

      for consumer in consumers:
	 for topic in consumer['topics']:
	    value = graphite_prefix + cluster.replace('.','_') + '.' + cons.replace('.','_') + '.' + topic.replace('.','_')
	    message = '%s %s %d' % (value, consumer['lags'][topic], timestamp)
	    metrics.append(message)

   return metrics

def send_graphite_metrics(message,graphite_host,graphite_port):
   print 'sending message:\n%s' % message
   sock = socket.socket()
   sock.connect((graphite_host,graphite_port))
   sock.sendall(message)
   sock.close() 


def main():

   # store some static params from config
   config = ConfigParser.SafeConfigParser()
   config.read(os.path.dirname(__file__) + '/consumer_lag.ini')

   base_url = config.get('api','url')

   bulk = prepare_graphite_metrics(base_url,config.get('graphite','prefix'))
   message = '\n' . join(bulk) + '\n'

   send_graphite_metrics(message,config.get('graphite','host'),int(config.get('graphite','port')))

if __name__ == "__main__":
   main()
