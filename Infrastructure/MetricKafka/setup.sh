#!/bin/bash
wget http://apache.spinellicreations.com/kafka/2.2.0/kafka_2.12-2.2.0.tgz
tar -xzf kafka_2.12-2.2.0.tgz
rm kafka_2.12-2.2.0/config/zookeeper.properties
rm kafka_2.12-2.2.0/config/server.properties
mv zookeeper.properties kafka_2.12-2.2.0/config/zookeeper.properties
mv server.properties kafka_2.12-2.2.0/config/server.properties
sudo apt-get install python-pip
pip install requests
