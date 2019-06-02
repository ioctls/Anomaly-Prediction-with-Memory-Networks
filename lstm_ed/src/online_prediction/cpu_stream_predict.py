from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import csv
from sklearn.preprocessing import MinMaxScaler
import math
import time
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import fbeta_score
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
from lstm_enc_dec_axl import LSTMED
from sklearn.model_selection import train_test_split
import torch 

window_size = 2
seeds = np.random.randint(np.iinfo(np.uint32).max, size=1, dtype=np.uint32)
instance = LSTMED(num_epochs=40, seed=seeds[0], sequence_length=window_size)

ip = "152.46.18.175"
port = 9092


host_1 = 'kafkaApplication_server1'
host_2 = 'kafkaApplication_server2'

rubis = 'RUBisApp'
also_rubis = 'responsetimeRubisApp'

bootstrap_servers = ip + ":" + str(port)

instance.lstmed = torch.load('../../models/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl')
print(instance.lstmed.threshold)
threshold = instance.lstmed.threshold

window = []
while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='latest', bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([host_2])
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                #response = {.. 'host', 'interval', 'plugin', 'time', 'values', 'type_instance'..}
                host = response["host"]
                plugin = response["plugin"]
                if(plugin != 'cpu'):
                    continue;
                items = response["values"]
                item = items[0]
                timestamp = response["time"]
                type_instance = response["type_instance"]

                clms = [plugin]


                if len(window) < window_size:
                    window.append(item)
                    if len(window) == window_size:
                        score=instance.predict(pd.DataFrame(window, columns=clms))
                        if(np.max(score) > threshold):
                            print(host, timestamp, item, "anomaly")
                        else:
                            print(host, timestamp, item, "normal")
                else:
                    window.pop(0)
                    window.append(item)
                    score=instance.predict(pd.DataFrame(window, columns=clms))
                    if(np.max(score) > threshold):
                        print(host, timestamp, item, "anomaly")
                    else:
                        print(host, timestamp, item, "normal")

    except Exception as e:
        print("Error %s", (e))
        #keyboard interrupt not really needed
