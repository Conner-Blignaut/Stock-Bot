import sys, os
if "venv" not in sys.executable:
    os.execv(os.path.join(os.path.dirname(__file__),
     "venv", "Scripts", "python.exe"), [sys.executable, __file__])

import yfinance as yf
import pandas as pd

def load_yf_data(input):
    ticker = yf.Ticker(input)
    data = ticker.history(period="3mo")
    print(f"\n{data}")
    return data

yf_data = load_yf_data("CEG")

yf_data.info()

import matplotlib.pyplot as plt

yf_data.hist(bins=40, figsize=(12, 8))

plt.show()

def shuffle_and_split_data(data, test_ratio, rng):
    shuffled_indicies

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(yf_data.values)

train_ratio = 0.67
train_size = int(len(dataset) * train_ratio)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))

import numpy as np

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        b = dataset[i + look_back, 0]
        dataY.append(b)
    return np.array(dataX), np.array(dataY)

look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

model_code = 3
epochNo = 100
batchSize = 10

import tensorflow as tf
from tensorflow.keras.layers import Dense

if (model_code == 3):
    from tensorflow.keras.layers import GRU, Dense

    model =tf.keras.Sequential()
    model.add(GRU(4, input_shape=(look_back,1)))

    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochNo, batch_size=batchSize, verbose=2)
else:
    print("invalid model code, try a correct code, 1 or 2")

trainPredict = model.predict(trainX)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])

testPredict = model.predict(testX)

testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

from sklearn.metrics import mean_squared_error

trainScore = np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()