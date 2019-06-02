import requests
import random
import time
import sys

source = sys.argv[1]
dataval = 1000
data = {'sourceID': source}
#r = requests.post(url="http://152.46.18.218:8080/register", data=data)
#r = requests.post(url="http://152.46.18.218:8080/activate", data=data)
#resp_json = r.json()
#print (resp_json)
#if resp_json.get("status")=="error":
#    print (resp_json.get("message"))
#    sys.exit()
try:
    while (True):

        oper = random.randint(1, 3)


        if (oper < 3):
            randomval = random.randint(6, 10)

            dataval += randomval
        else:
            randomval = random.randint(1, 2)
            dataval -= randomval
        if dataval < 0:
            dataval += randomval
        data = {'sourceID': source,
                'data': round(dataval, 2)}
        r = requests.post(url="http://152.46.18.218:8080/stream", data=data)

        time.sleep(30)

finally:
    data = {'sourceID': source}
    # r = requests.post(url="http://152.46.18.218:8080/inactivate", data=data)
