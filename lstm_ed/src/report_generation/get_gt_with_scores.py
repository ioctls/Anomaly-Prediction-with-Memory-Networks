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
import time


#sizes = [2, 5, 7, 10, 12, 15, 20]
sizes = [2]

for window_size in sizes:
	##used mem 1 all
	#path_test = '../../data/anomalous_data/vm16-137.vcl.ncsu.edu_used_memory.txt'
	#model_path = '../../models/vm16-137.vcl.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'
	#path_pred = '../../reports/vm16-137.vcl.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##used mem 2 ws = 2
	#path_test = '../../data/anomalous_data/vclv98-84.hpc.ncsu.edu_used_memory.txt'
	#model_path = '../../models/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'
	#path_pred = '../../reports/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##used mem 3 ws = 2
	#path_test = '../../data/anomalous_data/vm17-187.vcl.ncsu.edu_used_memory.txt'
	#model_path = '../../models/vm17-187.vcl.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'
	#path_pred = '../../reports/vm17-187.vcl.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##active cpu 1 all
	#path_test = '../../data/anomalous_data/vm16-137.vcl.ncsu.edu_active_cpu.txt'
	#model_path = '../../models/vm16-137.vcl.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'
	#path_pred = '../../reports/vm16-137.vcl.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'
	
	#active cpu 2 ws = 2
	path_test = '../../data/anomalous_data/vclv98-84.hpc.ncsu.edu_active_cpu.txt'
	model_path = '../../models/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'
	path_pred = '../../reports/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##active cpu 3 ws = 2
	#path_test = '../../data/anomalous_data/vm17-187.vcl.ncsu.edu_active_cpu.txt'
	#model_path = '../../models/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'
	#path_pred = '../../reports/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	seeds = np.random.randint(np.iinfo(np.uint32).max, size=1, dtype=np.uint32)
	instance = LSTMED(num_epochs=40, seed=seeds[0], sequence_length=window_size)

	X_test = pd.read_csv(path_test, sep=',', header=None)

	X_test = X_test.drop([0, 2], 1)

	instance.lstmed = torch.load(model_path)
	threshold = instance.lstmed.threshold

	print("window_size = ", window_size, "threshold = ", threshold)

	window = []

	clms = X_test.columns

	test = X_test.copy()

	file_pred = open(path_pred, 'w')

	for index, row in test.iterrows():
		item = row.values[0]
		timestamp=index
		if len(window) < window_size:
			window.append(item)
			if len(window) == window_size:
				score=instance.predict(pd.DataFrame(window, columns=clms.to_list()))
				if(np.max(score) > threshold):
					file_pred.write(str(item)+', 1, '+str(np.max(score))+'\n')
				else:
					file_pred.write(str(item)+', 0, '+str(np.max(score))+'\n')
					
		else:
			window.pop(0)
			window.append(item)
			score=instance.predict(pd.DataFrame(window, columns=clms.to_list()))
			if(np.max(score) > threshold):
				file_pred.write(str(item)+', 1, '+str(np.max(score))+'\n')
			else:
				file_pred.write(str(item)+', 0, '+str(np.max(score))+'\n')
	
	file_pred.close()
