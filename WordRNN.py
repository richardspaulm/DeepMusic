import warnings
warnings.simplefilter('ignore', FutureWarning)
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from math import ceil
from pprint import pprint
import re
SEQ_LENGTH = 50

def buildmodel(VOCAB):
    model = Sequential()
    model.add(LSTM(256, input_shape = (SEQ_LENGTH, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(VOCAB, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam') 
    return model

f = open("all_corp.txt", encoding='utf-8')
raw_text = f.read()
print("Subbing Text")
raw_text = re.sub("_", "x", raw_text)
print("Text subbed")


all_words = raw_text.split(" ")
word_len = len(all_words)
words = sorted(list(set(raw_text.split(" "))))
VOCAB = len(words)
print(VOCAB)
# exit()
text_length = len(raw_text)
vocab_len = len(words)

word_to_int = dict((w, i) for i, w in enumerate(words))
input_strings = []
output_strings = []

data = []
for i in range(len(all_words) - SEQ_LENGTH):
    X_seq = all_words[i:i+SEQ_LENGTH]
    X = [word_to_int[word] for word in X_seq]
    Y = word_to_int[all_words[i + SEQ_LENGTH]]
    X.append(Y)
    data.append(X)
data = np.array(data)
# print(data[0])
# exit()
len_seqs = len(input_strings)

# def custom_generator(data, batch_size = 64):
    
#     while True:
#           # Select files (paths/indices) for the batch
#           batch_paths = data[np.random.choice(data.shape[0], size=batch_size)]
#           batch_input = []
#           batch_output = [] 
          
#           # Read in each input, perform preprocessing and get labels
#           for inp in batch_paths:
#               batch_input += [ inp[:len(inp) - 1] ]
#               batch_output += [ inp[-1] ]
#           # Return a tuple of (input,output) to feed the network
#           batch_x = np.array( batch_input )
#           batch_x = batch_x.reshape(batch_x.shape[0], batch_x.shape[1], 1)
#           batch_y = np.array( batch_output )
#           print(batch_x.shape)
#           print(batch_y.shape)
#           yield( batch_x, batch_y )

input_arrays = np.array(input_strings)
input_arrays = np.reshape(input_arrays, (input_arrays.shape[0], input_arrays.shape[1], 1))
input_arrays = input_arrays/float(VOCAB)

output_arrays = np.array(output_strings)
output_arrays = np_utils.to_categorical(output_arrays)
print(input_arrays.shape)
print(output_arrays.shape)
# print(output_arrays)
model = buildmodel(VOCAB)
print(model.summary())
filepath="saved_models/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

n_points = len(data)
steps_per_epoch = ceil(n_points / 64)
print("Fitting Model")
# history = model.fit_generator(
#     generator=custom_generator(data),
#     epochs=50,
#     callbacks=callbacks_list,
#     steps_per_epoch=steps_per_epoch
# )

history = model.fit(input_arrays, output_arrays, epochs = 50, batch_size = 128, callbacks = callbacks_list)
for key in history.history.keys():
	try:
		pyplot.plot(history.history[key], label=key)
	except:
		print(key)
pyplot.legend()
pyplot.show()
model.save("final_rnn.hdf5")
# evaluate
print("Completed")
