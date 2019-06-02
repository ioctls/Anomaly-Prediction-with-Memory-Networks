#!/bin/bash
kafka_2.12-2.2.0/bin/zookeeper-server-start.sh -daemon kafka_2.12-2.2.0/config/zookeeper.properties
kafka_2.12-2.2.0/bin/kafka-server-start.sh  -daemon  kafka_2.12-2.2.0/config/server.properties
sudo service collectd stop
sudo service collectd start
java -jar producer.jar &
