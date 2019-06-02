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
from sklearn.metrics import accuracy_score, fbeta_score, balanced_accuracy_score, roc_auc_score
from sklearn.metrics import precision_recall_fscore_support as prf
from sklearn.metrics import roc_curve, auc
from tabulate import tabulate
import sys

def get_scores(y_true: list, y_pred: list):
	accuracy = accuracy_score(y_true, y_pred)
	precision, recall, f_score, _ = prf(y_true, y_pred, average='binary', warn_for=())
	if precision == 0 and recall == 0:
		f01_score = 0
	else:
		f01_score = fbeta_score(y_true, y_pred, average='binary', beta=0.1)

	balanced_accuracy = balanced_accuracy_score(y_true, y_pred)
	return accuracy, precision, recall, f_score, f01_score, balanced_accuracy

#sizes = [2, 5, 7, 10, 12, 15, 20]
sizes = [2]
#window_size = 10
for window_size in sizes:
        #make sure your paths are correct

	##used mem 1 all
	#host = 'vm16-137'
	#m_type = 'mem'
	#scores_path = '../../reports/scores_vm16-137.vcl.ncsu.edu_used_memorylatest_latest_anomalous_ws'+str(window_size)+'.txt'
	#path_gt = '../../reports/vm16-137.vcl.ncsu.edu_used_memorylatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	#path_pred = '../../reports/vm16-137.vcl.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##used mem 2 ws = 2
	#host = 'vclv98-84'
	#m_type = 'mem'
	#scores_path = '../../reports/scores_vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_anomalous_ws'+str(window_size)+'.txt'
	#path_gt = '../../reports/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	#path_pred = '../../reports/vclv98-84.hpc.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##used mem 3 ws = 2
	#host = 'vm17-187'
	#m_type = 'mem'
	#scores_path = '../../reports/scores_vm17-187.vcl.ncsu.edu_used_memorylatest_latest_anomalous_ws'+str(window_size)+'.txt'
	#path_gt = '../../reports/vm17-187.vcl.ncsu.edu_used_memorylatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	#path_pred = '../../reports/vm17-187.vcl.ncsu.edu_used_memorylatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	       
	##active cpu 1 all
	#host = 'vm16-137'
	#m_type = 'cpu'
	#scores_path = '../../reports/scores_vm16-137.vcl.ncsu.edu_active_cpulatest_latest_anomalous_ws'+str(window_size)+'.txt'
	#path_gt = '../../reports/vm16-137.vcl.ncsu.edu_active_cpulatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	#path_pred = '../../reports/vm16-137.vcl.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	##active cpu 2 ws = 2
	#host = 'vclv98-84'
	#m_type = 'cpu'
	#scores_path = '../../reports/scores_vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_anomalous_ws'+str(window_size)+'.txt'
	#path_gt = '../../reports/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	#path_pred = '../../reports/vclv98-84.hpc.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'

	#active cpu 3 ws = 2
	host = 'vm17-187'
	m_type = 'cpu'
	scores_path = '../../reports/scores_vm17-187.vcl.ncsu.edu_active_cpulatest_latest_anomalous_ws'+str(window_size)+'.txt'
	path_gt = '../../reports/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_anomalous_gt_ws'+str(window_size)+'.txt'
	path_pred = '../../reports/vm17-187.vcl.ncsu.edu_active_cpulatest_latest_anomalous_pred_ws'+str(window_size)+'.txt'


	if(window_size==sizes[0]):
		write_scores_to = open(scores_path, 'w')       
		write_scores_to.write('window_size\taccuracy\tbalanced_accuracy\tprecision\trecall\tf_score\tf01_score\ttpr\tfpr\tauc\n')

	gt_df = pd.read_csv(path_gt, sep=',', header=None)
	pred_df = pd.read_csv(path_pred, sep=',', header=None)

	gt_df = gt_df.drop([0], 1)
	pred_df = pred_df.drop([0], 1)

	accuracy, precision, recall, f_score, f01_score, balanced_accuracy = get_scores(list(gt_df[1]), list(pred_df[1]));

	#print(window_size, accuracy, balanced_accuracy, precision, recall, f_score, f01_score)

	#print(len(list(pred_df[2])), len(list(gt_df[1])))
	

	#using scores
	fpr, tpr, thresh = roc_curve(list(gt_df[1]), list(pred_df[2]))
	auc = roc_auc_score(list(gt_df[1]), list(pred_df[2]))

	##using y_pred (binary predictions)
	#fpr, tpr, thresh = roc_curve(list(gt_df[1]), list(pred_df[1]))
	#auc = roc_auc_score(list(gt_df[1]), list(pred_df[1]))

	#print(fpr, tpr, thresh, auc)


	write_scores_to.write(str(np.around(window_size, 2))+'\t'+str(np.around(accuracy, 2))+'\t'+str(np.around(balanced_accuracy, 2))+'\t'+str(np.around(precision, 2))+'\t'+str(np.around(recall, 2))+'\t'+str(np.around(f_score, 2))+'\t'+str(np.around(f01_score, 2))+'\t'+str(np.around(tpr, 2))+'\t'+str(np.around(fpr, 2))+'\t'+str(np.around(auc, 2))+'\n')
        

	plt.plot(fpr, tpr, color='darkorange',
		 lw=2, label='ROC Curve (area = %0.2f)' % auc)

	plt.xlabel('False positive')
	plt.ylabel('True positive')
	plt.title('ROC for window size = '+str(window_size))
	plt.legend(loc="lower right")
	plt.savefig('./figures/'+m_type+'/'+host+'_roc_ws_'+str(window_size))

	plt.close()

        #precision recall curve
	precision, recall, _ = precision_recall_curve(list(gt_df[1]), list(pred_df[2]))
	auc = average_precision_score(list(gt_df[1]), list(pred_df[2]))

	plt.plot(precision, recall, color='darkorange',
		 lw=2, label='PR Curve (area = %0.2f)' % auc)

	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.title('PR for window size = '+str(window_size))
	plt.legend(loc="lower right")
	plt.savefig('./figures/'+m_type+'/'+host+'_pr_ws_'+str(window_size))

	plt.close()
