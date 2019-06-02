#!/usr/bin/env python
# coding: utf-8

# In[1]:


from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

ip = "152.46.18.240"
port = 9092

host_1 = 'kafkaApplication_server1'
host_2 = 'kafkaApplication_server2'
rubis = 'RUBisApp'
also_rubis = 'responsetimeRubisApp'

bootstrap_servers = ip + ":" + str(port)
consumer = KafkaConsumer(auto_offset_reset='earliest',
                                        bootstrap_servers=[bootstrap_servers])
consumer.subscribe([host_1, host_2, rubis, also_rubis])
path = "data/"

while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='earliest',
                                        bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([host_1, host_2, rubis])
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                host = response["host"]
                plugin = response["plugin"]
                items = response["values"]
                timestamp = response["time"]
                type_instance = response["type_instance"]
                if(type_instance != "active"):
                    if(type_instance != "used"):
                        continue

                if(timestamp < 1556897417.589):
                    continue
                filename = path + host + "_" + type_instance + "_" + plugin + ".txt"
                with open(filename, "a") as f:
                    f.write(str(timestamp) + ",")
                    for item in items:
                        f.write(str(item) + ",")
                    f.write("\n")
    except Exception as e:
        print("Error %s", (e))
