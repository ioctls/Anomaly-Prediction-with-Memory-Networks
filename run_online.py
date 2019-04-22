#!/usr/bin/env python
# coding: utf-8

# In[1]:


from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from utils import lstm_encdec
import csv


# In[2]:


#152.46.18.175
#9092
ip = "152.46.18.175"
port = 9092


# In[17]:


host_1 = 'kafkaApplication_server1'
host_2 = 'kafkaApplication_server2'

rubis = 'RUBisApp'
also_rubis = 'responsetimeRubisApp'


# In[22]:


pdata = {}
bootstrap_servers = ip + ":" + str(port)
consumer = KafkaConsumer(auto_offset_reset='latest',
                                        bootstrap_servers=[bootstrap_servers])
consumer.subscribe([host_1, host_2, rubis, also_rubis])
#consumer.subscribe([rubis, also_rubis])


# In[8]:


while True:
    try:
        consumer = KafkaConsumer(auto_offset_reset='latest',
                                        bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([host_1, host_2, rubis, also_rubis])
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                #response = {.. 'host', 'interval', 'plugin', 'time', 'values', 'type_instance'..}
                host = response["host"]
                plugin = response["plugin"]
                items = response["values"]
                timestamp = response["time"]
                type_instance = response["type_instance"]
                filename = path + host + "_" + type_instance + "_" + plugin + ".txt"
                with open(filename, "a") as f:
                        f.write(str(timestamp) + ",")
                    for item in items:
                        f.write(str(item) + ",")
                    f.write("\n")
    except Exception as e:
        print("Error %s", (e))
        #keyboard interrupt not really needed


# In[9]:


lop = {}
try:
    y = lop["cat"]
except KeyError:
    lop["cat"] = {"black" : 1, "white" : 1}

try:
    y = lop["cat"]["black"]
except KeyError:
    lop["cat"]["black"] = 1
    
print(y + 1)


# In[10]:


#machine models[response["host"]]


# In[11]:


window_size = 5
input_dim = 1
hidden_dim = 12
models = {}


# In[12]:


primary_epochs = 15
online_epochs = 5


# In[13]:


#1, collect data, 2, train, 3, deploy
#or
#train on go



#def threshold is None
#cannot updtate with micro updates
#need some default value or training data


# In[15]:


window = []
while True:
    try:
        consumer = KafkaConsumer(topic, auto_offset_reset='latest',
                                        bootstrap_servers=[bootstrap_servers])
        consumer.subscribe([topic])
        while True:
            for msg in consumer:
                response = json.loads(msg.value.decode('utf-8'))[0]
                #response = {.. 'host', 'interval', 'plugin', 'time', 'values' ..}
                host = response["host"]
                plugin = response["plugin"]
                item = response["values"][0]
                print(response)
                try:
                    instance = models[host][plugin]
                except KeyError:
                    try:
                        instance = models[host]
                    except:
                        models[host] = {}
                    p = lstm_encdec(window_size, input_dim, hidden_dim)
                    #p.train_model(x_train, x_valid, primary_epochs)
                    models[host][plugin] = p
                
                instance = models[host][plugin]

                if len(window) < 5:
                    window.append(item)
                    if len(window) == 5:
                        instance.micro_update(window, online_epochs)
                        #print(item, instance.is_anomalous(window))
                        continue
                    
                else:
                    window.pop(0)
                    window.append(item)
                    #instance.micro_update(window, online_epochs)
                    #print(item, instance.is_anomalous(window))
                continue
                
    except Exception as e:
        print("Connection Error %s", (e))
        


# In[ ]:




