from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np
# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg
 
# load dataset
dataset = read_csv('k3_train/pollution.csv', header=0, index_col=0)
print(dataset.head())
exit()
columns_to_predict = 8


print(dataset.head())
# exit()
values = dataset.values
print(values)
# integer encode direction
encoder = LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4])
# ensure all data is float
values = values.astype('float32')
# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
# print(values.shape)
# exit()
scaled = scaler.fit_transform(values)
print(values)
print(values.shape)
# exit()
# frame as supervised learning
reframed = series_to_supervised(scaled, 10, 1)
print(reframed.head())
# drop columns we don't want to predict
# reframed.drop(reframed.columns[[12,13,14,15]], axis=1, inplace=True)
print(reframed.head())
print(reframed.shape)
# exit()
# split into train and test sets
values = reframed.values
n_train_hours = 365 * 72
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
# split into input and outputs
train_X, train_y = train[:, :values.shape[1] - columns_to_predict], train[:, -columns_to_predict:]
test_X, test_y = test[:, :values.shape[1] - columns_to_predict], test[:, -columns_to_predict:]

# reshape input to be 3D [samples, timesteps, features]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(8))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=20, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
 
# make a prediction
yhat = model.predict(test_X)
print(yhat)
print(yhat.shape)
# yhat = concatenate((np.zeros((yhat.shape[0], yhat.shape[1])), yhat),axis=1)
# print(yhat)
# print(yhat.shape)
# yhat = yhat.reshape(yhat.shape[0], 8, yhat.shape[1])
yhat = scaler.inverse_transform(yhat)


yhat = yhat[:, :columns_to_predict]
print(yhat)