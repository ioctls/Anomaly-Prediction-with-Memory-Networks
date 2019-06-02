from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import csv
import time

ip = "152.46.18.240"
port = 9092


host_1 = 'kafkaApplication_server1'
host_2 = 'kafkaApplication_server2'

rubis = 'RUBisApp'
also_rubis = 'responsetimeRubisApp'

bootstrap_servers = ip + ":" + str(port)

path = './latest/latest/'
flag = False
while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='smallest',
                                        bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([host_1, host_2, rubis])
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                #response = {.. 'host', 'interval', 'plugin', 'time', 'values', 'type_instance'..}
                host = response["host"]
                plugin = response["plugin"]
                items = response["values"]
                timestamp = response["time"]
                type_instance = response["type_instance"]
                if not (plugin == 'memory' and type_instance=='used'):
                    continue;
                if(timestamp < 1556727754.076):
                    if not flag:
                        print("Now collecting")
                        flag = True

                    filename = path + host + "_" + type_instance + "_" + plugin + "latest_latest.txt"
                    with open(filename, "a") as f:
                        f.write(str(timestamp) + ",")
                        for item in items:
                            f.write(str(item) + ",")
                        f.write("\n")
                elif(flag):
                    print("Done")
                    exit(0)
    except Exception as e:
        print("Error %s", (e))
        #keyboard interrupt not really needed
