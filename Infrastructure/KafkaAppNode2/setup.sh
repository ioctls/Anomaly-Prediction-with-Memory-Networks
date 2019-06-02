#!/bin/bash
wget http://apache.spinellicreations.com/kafka/2.2.0/kafka_2.12-2.2.0.tgz
tar -xzf kafka_2.12-2.2.0.tgz
rm kafka_2.12-2.2.0/config/zookeeper.properties
rm kafka_2.12-2.2.0/config/server.properties
mv zookeeper.properties kafka_2.12-2.2.0/config/zookeeper.properties
mv server.properties kafka_2.12-2.2.0/config/server.properties
mkdir /tmp/zookeeper
echo '2' > /tmp/zookeeper/myid
sudo iptables -F
sudo iptables -A INPUT -p tcp -j ACCEPT
sudo apt-get install collectd collectd-utils
sudo rm /etc/collectd/collectd.conf
sudo mv collectd.conf /etc/collectd/collectd.conf
