#!pip install -U "tensorflow-text==2.8.*"
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer,tokenizer_from_json
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding,Bidirectional
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
from keras.models import Sequential, load_model
import json



classes = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
       'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
       'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
       'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
       'relief', 'remorse', 'sadness', 'surprise', 'neutral']
with open("./IA/tokenizer.json") as file:
    data = json.load(file)
    tokenizer = tokenizer_from_json(data)
    
def prediction(sentence):
    sequence = tokenizer.texts_to_sequences([sentence])
    #pad sequence
    sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence,maxlen=142,padding='post')
    #feature = np.array([item for item in [seq for seq in sequence]])
    # load model
    with tf.device('/cpu:0'):
        Model = load_model('./IA/goemo.h5')
        pred = Model.predict(sequence)
    df = pd.DataFrame(pred,columns=classes)
    return df
    