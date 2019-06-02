#!/bin/bash
sudo iptables -F
sudo iptables -A INPUT -p tcp -j ACCEPT
sudo apt-get install collectd collectd-utils
sudo rm /etc/collectd/collectd.conf
sudo mv collectd.conf /etc/collectd/collectd.conf
sudo apt-get install mysql-server
sudo apt-get install apache2
sudo apt-get install php libapache2-mod-php php-mcrypt php-mysql
sudo apt-get install default-jdk
sudo apt-get install openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
export CLASSPATH=/usr/lib/jvm/java-8-openjdk-amd64/lib
cp -r RUBiS/PHP /var/www/html/
mv RUBiS ../../
sudo service collectd start
