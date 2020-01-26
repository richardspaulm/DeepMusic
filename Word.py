from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from matplotlib import pyplot
from keras.callbacks import ModelCheckpoint

import pickle
import re


## Read Source Text, format for encoding
with open("all_corp.txt", "r") as f:
    data = f.read().lower()
data = data.split(" ")

#Temporarily Decrease Data Size for quicker Training. Remove Splice Once models fit
data = data[:int(len(data) / 16)]
data = " ".join(data)
data = re.sub("_", "x", data)

#Fetching Seed
# data = data.split(" ")
# print(str(data[:30]))
# exit()

# integer encode text and save encoder for later use
tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
encoded = tokenizer.texts_to_sequences([data])[0]


# determine the vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print('Vocabulary Size: %d' % vocab_size)
# create word -> word sequences
sequences = list()

SEQUENCE_LEN = 30
X = list()
y = list()
for i in range(SEQUENCE_LEN, len(encoded)):
	x_seq = encoded[i-SEQUENCE_LEN:i]
	y_seq = encoded[i]
	X.append(x_seq)
	y.append(y_seq)
print('Total Sequences: %d' % len(X))
# Convert X and y to numpy arrays
X = array(X)
y = array(y)

# one hot encode outputs
y = to_categorical(y, num_classes=vocab_size)
# define model

model = Sequential()
model.add(Embedding(vocab_size, 32, input_length=SEQUENCE_LEN))
model.add(LSTM(50))
model.add(Dense(vocab_size, activation='tanh'))
print(model.summary())
# compile network
model.compile(loss='categorical_crossentropy', optimizer='adam')
# fit network
mc = ModelCheckpoint('weights{epoch:08d}.hdf5', 
                                     save_weights_only=True, period=5)
history = model.fit(X, y, epochs=1, verbose=2, validation_split=0.3, callbacks=[mc])
for key in history.history.keys():
	try:
		pyplot.plot(history.history[key], label=key)
	except:
		print(key)
	# pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
model.save("final_words.hdf5")
# evaluate
print("Completed")