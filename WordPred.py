from keras.models import load_model
import pickle
from numpy import array
import re
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Bidirectional, Embedding
# generate a sequence from the model
def generate_seq(model, tokenizer, seed_text, n_words):
    in_text, result = seed_text, seed_text
	# generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences(in_text)
        # print(encoded)
        encoded = [e[0] for e in encoded]
        # print(encoded)
        # exit()
        encoded = array(encoded)
        # print(encoded)
        encoded = encoded.reshape((1,30))
        # print(encoded.shape)
        # exit()
        # predict a word in the vocabulary
        yhat = model.predict_classes(encoded, verbose=1)[0]
		# map predicted word index to word
        out_word = None
        # print(tokenizer.word_index.items())
        # exit()
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
		# append to input
        result.append(out_word)
        print(out_word)
        in_text = result[-30:]
        # print(result)
    return result

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

vocab_size = len(tokenizer.word_index) + 1
SEQUENCE_LEN = 30

# model = model.load_model("finalmodel.hdf5")

model = Sequential()
model.add(Embedding(vocab_size, 128, input_length=SEQUENCE_LEN))
model.add(LSTM(10))
model.add(Dense(vocab_size, activation='softmax'))
model.load_weights("weights00000020.hdf5")


seed = ['cx0x64x0', 'px0x0', 'cx0x7x127', 'cx0x10x64', 'cx0x64x127', 'nx0x60x110', 'nx0x63x110', 'nx0x67x110', 'nx94x60x0', 'nx0x63x0', 'nx0x67x0', 'nx2x72x110', 'nx46x72x0', 'nx2x63x110', 'nx94x63x0', 'nx2x60x110', 'nx0x63x110', 'nx0x72x110', 'nx94x60x0', 'nx0x63x0', 'nx0x72x0', 'nx2x63x110', 'nx0x67x110', 'nx94x63x0', 'nx0x67x0', 'nx2x72x110', 'nx94x72x0', 'nx2x67x110', 'nx46x67x0', 'nx2x63x110']
text = generate_seq(model, tokenizer, seed, 600)
text = " ".join(text)
text = re.sub("x", "_", text)
with open("output_txt.txt", "w") as f:
    f.write(text)