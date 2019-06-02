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
path='./latest/latest/'

bootstrap_servers = ip + ":" + str(port)

while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='smallest',
                                        bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([also_rubis])
        flag = False
        rt_list = []
        while True:
            for msg in consumer:
                rt, ts = (msg.value.decode()).split(',')
                ts = int(ts)
                rt = int(rt)

                host = "vm16-137"
                filename = path + host + "_latest_latest_rt_rubis_normal.txt"
                if(ts < 1556727754.076):# and ts < 1556832577):
                    if not flag:
                        print("Now collecting")
                    flag = True
                    rt_list.append((ts, rt))
                elif(flag):
                    print("Sorting")
                    rt_list.sort()
                    f=open(filename, 'w')
                    #fo_flag = True
                    print("Writing to file")

                    for each in rt_list:
                        f.write(str(each[0]) + ",")
                        f.write(str(each[1]) + ",")
                        f.write("\n")

                    print("Done")
                    exit(0)
    except Exception as e:
        print("Error %s", (e))
        #keyboard interrupt not really needed

