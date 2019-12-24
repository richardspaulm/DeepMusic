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
from math import ceil
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

dataset = read_csv("k3_train/full_midi.csv", index_col=0)
print(dataset.head())
columns_to_predict = 3

values = dataset.values
print(values)
# encoder = LabelEncoder()
# values[:,3] = encoder.fit_transform(values[:,3])

values = values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))

scaled = scaler.fit_transform(values)
print(values)

reframed = series_to_supervised(scaled, 20, 1)
print(reframed.head())

values = reframed.values

n_train_rows = int(len(values) * .75)
train = values[:n_train_rows, :]
test = values[n_train_rows:, :]

train_X, train_y = train[:, :values.shape[1] - columns_to_predict], train[:, -columns_to_predict:]
test_X, test_y = test[:, :values.shape[1] - columns_to_predict], test[:, -columns_to_predict:]

# reshape input to be 3D [samples, timesteps, features]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

model = Sequential()
model.add(LSTM(200,input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(3))
model.compile(loss='mae', optimizer='adagrad')
# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=128, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
model.save("final_model.hdf5")
pyplot.show()
def round_of_rating(number):
    return [ceil(num) for num in number]    

print("Predicting")
yhat = model.predict(train_X[:200])
print("Inverting Scale")
yhat = scaler.inverse_transform(yhat)
# y = encoder.inverse_transform(round_of_rating(yhat[:, 3]))
# print(y)

df = DataFrame(yhat)
# output = np.zeros(yhat.shape)
# # output[:, 3] = yhat[:, 3].astype(str)
# # output[:, :3] = yhat[:, :3]
# df = DataFrame(output)
# print(df)
# nrows = len(df.iloc[:, 0])

# def round_df(df, cols=3):
#     for i in range(cols):
#         nrows = len(df.iloc[:, i])
#         for j in range(nrows):
#             df.iloc[j, i] = int(df.iloc[j, i])

# # for i in range(nrows):
#     # df.iloc[i, 3] = y[i]

# # for r in ran/ge(nrows):
#     # for c in range(3):
#         # df.iloc[r, c] = int(df.iloc[r,c])

# # df = round_df(df)
# print(df)
df.to_csv("mid_predictions.csv")