from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import csv

ip = "152.46.18.175"
port = 9092


host_1 = 'kafkaApplication_server1'
host_2 = 'kafkaApplication_server2'

rubis = 'RUBisApp'
also_rubis = 'responsetimeRubisApp'
path='./'

bootstrap_servers = ip + ":" + str(port)

while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='smallest',
                                        bootstrap_servers=[bootstrap_servers])
        #consumer.subscribe([host_1, host_2, rubis, also_rubis])
        consumer.subscribe([host_2])
        flag = False
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                #response = {.. 'host', 'interval', 'plugin', 'time', 'values', 'type_instance'..}
                host = response["host"]
                plugin = response["plugin"]
                items = response["values"]
                timestamp = response["time"]
                type_instance = response["type_instance"]
                filename = path + host + "_" + type_instance + "_" + plugin + "_1s_normal_mem+cpu_latest.txt"
                if(timestamp > 1556169450.445 and timestamp < #1556163711.296):
                    flag = True
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

