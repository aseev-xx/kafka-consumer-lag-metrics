# Kafka consumer lag metrics
Simple parser kafka consumer lag metrics from kafka-manager api and send to graphite

## Getting started

### Prerequisites
Kafka-manager Routes: https://github.com/yahoo/kafka-manager/blob/master/conf/routes

### Usage
```
$ python ./consumer_lag.py
```

Simple output:
```
sending message:
prefix.graphite.kafka_cluster_1.development-consumer-1.dev-topic1 1234 1553678915
prefix.graphite.kafka_cluster_1.development-consumer-1.dev-topic2 110 1553678915
prefix.graphite.kafka_cluster_1.production-consumer-1.prod-topic1 0 1553678915
prefix.graphite.kafka_cluster_1.production-consumer-2.prod-topic2 0 1553678915
prefix.graphite.kafka_cluster_2.test-consumer-1.test-topic1 1111 1553678915
prefix.graphite.kafka_cluster_2.test-consumer-1.test-topic2 2222 1553678915
...
```

### Configuration
Before starting you need to open api in kafka-manager application.conf
(for more detail see https://github.com/yahoo/kafka-manager/blob/master/conf/application.conf#L64):
```
basicAuthentication.excluded=["/api/health","/api/status/.*"] # ping the health of your instance without authentification
```
