#!/usr/bin/env python
# coding: utf-8

from keras.layers import RepeatVector
from keras.layers.core import Dropout, Dense, Activation
from keras.layers.recurrent import LSTM, GRU
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from sklearn.preprocessing import MinMaxScaler
import math
import time
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import fbeta_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import *
from scipy import stats


def get_data():
    path = "fastStorage/fastStorage/2013-8/1.csv"
    df = pd.read_csv(path, sep=';\t')
    df = df.drop(['CPU cores', 'Memory capacity provisioned [KB]'], 1)
    if(df.isnull().sum().sum()):
        df = df.fillna(df.mean())
    return df


def get_benchmark():
    path = "datasets/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark/real_59.csv"
    #path = "ydata-labeled-time-series-anomalies-v1_0/A3Benchmark/A3Benchmark_all.csv"
    df = pd.read_csv(path, sep=',')
    df = df.drop(['timestamp', 'is_anomaly'], 1)
    if(df.isnull().sum().sum()):
        df = df.fillna(df.mean())
    return df


def make_data_windows(data, window_length=12):
    train_windows = []
    for window_start in range(0, len(data) - window_length + 1):
        window_end = window_start + window_length
        window_range = range(window_start, window_end)
        window = list(data[window_range])
        train_windows.append(window)
    return train_windows


def orchestrate_data(data, window_size, ltrain, lvalid, ltest):
    signal = data
    length = signal.shape[0]
    slicet = int(ltrain*(length))
    slicev = slicet + int(lvalid*(length))
    signal_train = signal[:slicet]
    signal_valid = signal[slicet:slicev]
    signal_test = signal[slicev:length]
    xtrain = np.array(make_data_windows(signal_train, window_size))
    xvalid = np.array(make_data_windows(signal_valid, window_size))
    xtest = np.array(make_data_windows(signal_test, window_size))
    return xtrain, xvalid, xtest


def modelgru(window_length, input_dim=1, hidden_dim=12):
    input_length = window_length
    m = Sequential()
    m.add(GRU(units=2 * hidden_dim, activation='relu', input_shape=(input_length, input_dim), return_sequences=True))
    m.add(Dropout(rate=0.2))
    m.add(GRU(units=hidden_dim, activation='relu', input_shape=(input_length, input_dim), return_sequences=True))
    m.add(Dropout(rate=0.1))
    m.add(GRU(units=hidden_dim, activation='relu', input_shape=(input_length, input_dim),return_sequences=True))
    m.add(Dropout(rate=0.1))
    m.add(GRU(units=2 * hidden_dim, activation='relu', input_shape=(input_length, input_dim),return_sequences=True))
    m.add(Dropout(rate=0.2))
    m.add(Dense(input_dim))
    m.compile(loss='mse', optimizer='adam')
    return m


def plot_reconstruction(history):
    plt.figure(figsize=(22, 4))
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'valid'], loc='best')
    plt.show()
    return


class lstm_encdec():
    def __init__(self, window_size, input_dim, hidden_dim):
        
        self.model = modelgru(window_size, input_dim, hidden_dim)
        self.window_size = window_size
        self.train_time = None
        self.threshold = None
        self.update_time = 0
        self.update_count = 0
        self.input_dim = input_dim
        self.checkpointer = ModelCheckpoint(filepath="lstm.autoencoder.weights.best.hdf5",
                                       verbose=1, save_best_only=True)
        self.earlystopper = EarlyStopping(monitor='val_loss', patience=5, verbose=0)
        
    def train_model(self, x_train, x_valid, epochs):

        tbCallBack = TensorBoard(log_dir='lstm.autoencoder.tb.graph',
                                 histogram_freq=0, write_graph=True, write_images=True)

        start_time = time.time()
        history = self.model.fit(x_train, x_train, batch_size=self.window_size,
                                epochs=epochs, validation_data=(x_valid, x_valid), 
                                callbacks=[self.checkpointer, self.earlystopper, tbCallBack], verbose=0).history
        end_time = time.time()
        self.train_time = (end_time - start_time)
        plot_reconstruction(history)
        
        pred_x = self.model.predict(x_train)
        max_mae_of_predictions = np.squeeze(np.max(np.square(x_train[:,:,:] - pred_x[:,:,:]), axis=1))
        max_mae_threshold = np.mean(max_mae_of_predictions) + 3*np.std(max_mae_of_predictions)
        self.threshold = max_mae_threshold
        
        return history
    
    def train_batch(self, data, epochs, slicetr, slicev, slices):
        xtrain, xvalid, xtest = orchestrate_data(dataa, self.window_size, slicetr, slicev, slices)
        return instance.train_model(xtrain, xvalid, epochs) 
    
    def plot_scope(self, data):
        xtrain, xvalid, xtest = orchestrate_data(data, self.window_size, 1.0, 0.0, 0.0)
        predx = self.model.predict(xtrain)
        
        signal = data
        if signal.shape[1] > 1:
            investigate_multi_errors(xtrain, predx, signal, self.window_size)
        else:
            investigate_errors(xtrain, predx, signal, self.window_size)
        return
              
    def predict(self, data):
        y = np.reshape(np.array(data), (1, self.window_size, self.input_dim))
        return self.model.predict(y)
    
    def update_threshold(self, data):
        xtrain, xvalid, xtest = orchestrate_data(data, self.window_size, 1.0, 0.0, 0.0)
        predx = self.model.predict(xtrain)
        
        max_mae_of_predictions = np.squeeze(np.max(np.square(xtrain[:, :, :] - predx[:, :, :]), axis=1))
        max_mae_threshold = np.mean(max_mae_of_predictions) + 3*np.std(max_mae_of_predictions)
        self.threshold = max_mae_threshold
        return
        
    def is_anomalous(self, data):
        y = np.reshape(np.array(data), (1, self.window_size, self.input_dim))
        pred = self.model.predict(y)
            #max for each window is taken
            #avg for each window is taken
            #squeeze just eliminated redundant dimention of 1
            #max for each window we have and mean for each window we have
        max_mae = np.squeeze(np.max(np.square(y[:,:,:] - pred[:,:,:]), axis=1))

        if(self.threshold < max_mae):
            return "anomaly"
        else:
            return "benign"
    
    def micro_update(self, point, epochs):
        y = np.reshape(np.array(point), (1, self.window_size, self.input_dim))
        start_time = time.time()
        self.model.fit(y, y, batch_size=self.window_size, epochs=epochs, verbose=0)
        end_time = time.time()
        self.update_time += (end_time - start_time)
        self.update_count += 1
        return


def investigate_errors(x_test, pred_x_test, signal_test=None, window_length=None):
    max_mae_of_predictions = np.squeeze(np.max(np.square(x_test[:,1:,:] - pred_x_test[:,1:,:]), axis=1))
    avg_mae_of_predictions = np.squeeze(np.mean(np.square(x_test[:,1:,:] - pred_x_test[:,1:,:]), axis=1))
    df = pd.DataFrame(data=np.c_[max_mae_of_predictions, avg_mae_of_predictions], 
                  columns=['max_mae_of_predictions', 'avg_mae_of_predictions'])
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 4))
    df['max_mae_of_predictions'].plot.hist(bins=50, ax=ax[0])
    df['max_mae_of_predictions'].plot.kde(secondary_y=True, ax=ax[0])
    ax[0].set_title('max_mae_of_predictions distribution')
    df['avg_mae_of_predictions'].plot.hist(bins=50, ax=ax[1])
    df['avg_mae_of_predictions'].plot.kde(secondary_y=True, ax=ax[1])
    ax[1].set_title('avg_mae_of_predictions distribution');
    kernel_max_mae = stats.gaussian_kde(df['max_mae_of_predictions'].values)
    kernel_avg_mae = stats.gaussian_kde(df['avg_mae_of_predictions'].values)
    df['pdf_max_mae'] = df['max_mae_of_predictions'].map(lambda x: kernel_max_mae.integrate_box(x - 1e-8, x + 1e-8))
    df['pdf_avg_mae'] = df['avg_mae_of_predictions'].map(lambda x: kernel_avg_mae.integrate_box(x - 1e-8, x + 1e-8))
    max_mae_threshold = np.mean(max_mae_of_predictions) + np.std(max_mae_of_predictions)
    
    plt.figure(figsize=(22, 4))
    df['max_mae_of_predictions'].plot()
    plt.axhline(y=max_mae_threshold, color='orange', label='threshold')
    plt.legend(loc='best')
    plt.title('max_mae_of_predictions_per_window')
    plt.grid(True, which='both');

    pred_outlier_indices = np.where(max_mae_of_predictions > max_mae_threshold)[0]
    plt.figure(figsize=(22, 4))
    plt.plot(signal_test)
    for w_index in pred_outlier_indices:
        plt.fill_betweenx((signal_test.min(), signal_test.max()), w_index, w_index + window_length - 1, alpha=0.1, color='red')
    plt.title('Anomalous Windows')
    plt.grid(True);


def investigate_multi_errors(x_test, pred_x_test, signal_test, window_length):
    
    max_mae_of_predictions = np.squeeze(np.max(np.square(x_test[:,:,:] - pred_x_test[:,:,:]), axis=1))
    max_mae_threshold = np.mean(max_mae_of_predictions) + np.std(max_mae_of_predictions)
    pred_outlier_indices = np.where(max_mae_of_predictions > max_mae_threshold)[0]
    
    plt.figure(figsize=(22, 4))
    plt.plot(signal_test)
    for w_index in pred_outlier_indices:
        plt.fill_betweenx((signal_test.min(), signal_test.max()), w_index, w_index + window_length - 1, alpha=0.1, color='orange')
    plt.title('Anomalous Windows')


def get_data_actual():
    path = "mem.txt"
    df = pd.read_csv(path, sep=',', header=None)
    df = df.drop([0], 1)
    if(df.isnull().sum().sum()):
        df = df.fillna(df.mean())
    return df


if __name__ == "__main__":
    window_size = 5
    input_dim = 1
    hidden_dim = 12
    instance = lstm_encdec(window_size, input_dim, hidden_dim)
    print("Module used by other scripts") 
