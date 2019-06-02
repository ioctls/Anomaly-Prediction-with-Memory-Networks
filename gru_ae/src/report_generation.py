#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score, auc
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_curve, precision_recall_fscore_support


def get_df2(file):
    path = "experiments/"
    df = pd.read_csv(path + file, sep=',', header=None)
    df = df.dropna()
    return df

def transform_cpu(df):
    df[1] = df[1].astype('category').cat.codes
    df[1] = 1 - df[1]
    df[2] = np.square(df[0] - df[2])
    df[0] = np.where(df[0] > 79, 1, 0)
    #print(df.head)
    return df

def transform_mem(df):
    df[1] = df[1].astype('category').cat.codes
    df[1] = 1 - df[1]
    df[2] = np.square(df[0] - df[2])
    df[0] = np.where(df[0] > 69, 1, 0)
    #print(df.head)
    return df

def pull_files():
    path = "experiments/"
    l = os.listdir(path)
    dfs = {}
    for item in l:
        items = item.split("_")
        if(len(items) > 1):
            string = items[0] + "_" + items[1] + "_" + items[4]
            #print(string)
            df = get_df2(item)
            if(items[1] == "active"):
                df = transform_cpu(df)
            else:
                df = transform_mem(df)
            dfs[string] = df
    return dfs

def find_scores_with_scores(df, win, save_location):
    #roc_curve, roc_auc_score
    if(save_location == "mem"):
        path = "results/memory/"
    else:
        path = "results/cpu/"
        
    y_true = df[1]
    y_scores = df[2]
    
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    area = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.2f)' % area)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC for window size = %d' % (win))
    plt.legend(loc="lower right")
    plt.savefig(path + str(win) + "_" + save_location + ".png")
    
    return area
    
def find_scores(df):
    y_true = df[0]
    y_pred = df[1]
    acc = accuracy_score(y_true, y_pred)
    bas = balanced_accuracy_score(y_true, y_pred)
    f1s = f1_score(y_true, y_pred)
    prfs = precision_recall_fscore_support(y_true, y_pred, average='binary')
    return acc, bas, f1s, prfs

def generate_results():
    presult = "results/results.txt"
    fx = open(presult, "w")
    dfs = pull_files()
    
    
    fx.write("CPU\n")
    fx.write("window_size\taccuracy  balanced_accuracy   precision\t\trecall\t\tf1_score\tauc\n")
    for i in dfs.keys():
        iss = i.split("_")
        if "active" in i:
            acc, bas, f1s, prfs = find_scores(dfs[i])
            auc = find_scores_with_scores(dfs[i], int(iss[2]), "cpu")
            fx.write("%s\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\n" % (iss[2], acc, bas, prfs[0], prfs[1], f1s, auc))
        
        
    fx.write("\n\nMemory\n")
    fx.write("window_size\taccuracy  balanced_accuracy   precision\t\trecall\t\tf1_score\tauc\n")
    for i in dfs.keys():
        iss = i.split("_")
        if "used" in i:
            acc, bas, f1s, prfs = find_scores(dfs[i])
            auc = find_scores_with_scores(dfs[i], int(iss[2]), "mem")
            fx.write("%s\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\t\t%0.2f\n" % (iss[2], acc, bas, prfs[0], prfs[1], f1s, auc))
            
    file = "experiments/outcomes.txt"
    with open(file) as f:
        l = f.readlines()
    fx.write("\nCPU\n")
    fx.write("window_size\tonline updation cost\n")
    for item in l:
        v = item.split("_")
        if v[1] == "active":
            parse = v[4]
            parse = parse.split("0.0")
            fx.write("%d\t\t%0.3f%s\n" % (int(parse[0]), float("0.0" + parse[1][:-1]), " secs"))
        
    fx.write("\nMemory\n")
    fx.write("window_size\tonline updation cost\n")
    for item in l:
        v = item.split("_")
        if v[1] == "used":
            parse = v[4]
            parse = parse.split("0.0")
            fx.write("%d\t\t%0.3f%s\n" % (int(parse[0]), float("0.0" + parse[1][:-1]), " secs"))


if __name__ == "__main__":
    generate_results()

