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
sizes = [2] #best window size according to results

for window_size in sizes:
	##used mem 1 all
	#path_train = '../../data/training_data/vm16-137.vcl.ncsu.edu_used_memorylatest_latest.txt'
	#model_path = '../../models/vm16-137.vcl.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'

	##used mem 2 only ws=2
	#path_train = '../../data/training_data/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest.txt'
	#model_path = '../../models/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'

	#used mem 3 only ws=2
	path_train = '../../data/training_data/vm17-187.vcl.ncsu.edu_used_memorylatest_latest.txt'
	model_path = '../../models/vm17-187.vcl.ncsu.edu_used_memorylatest_latest_normal_ws_'+str(window_size)+'.pkl'

	##active cpu 1 all
	#path_train = '../../data/training_data/vm16-137.vcl.ncsu.edu_active_cpulatest_latest.txt'
	#model_path = '../../models/vm16-137.vcl.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'

	##active cpu 2 only ws=2
	#path_train = '../../data/training_data/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest.txt'
	#model_path = '../../models/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'

	##active cpu 3 only ws=2
	#path_train = '../../data/training_data/vm17-187.vcl.ncsu.edu_active_cpulatest_latest.txt'
	#model_path = '../../models/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_normal_ws_'+str(window_size)+'.pkl'
	

	seeds = np.random.randint(np.iinfo(np.uint32).max, size=1, dtype=np.uint32)
	instance = LSTMED(num_epochs=40, seed=seeds[0], sequence_length=window_size)

	X_train = pd.read_csv(path_train, sep=',', header=None)

	X_train = X_train.drop([0, 2], 1)


	instance.fit(X_train.copy())
	torch.save(instance.lstmed, model_path)

	instance.lstmed = torch.load(model_path)
	threshold = instance.lstmed.threshold
	print("window_size = ", window_size, "threshold = ", threshold)
