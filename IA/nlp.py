from gensim.models import Word2Vec,FastText,KeyedVectors 
import re
import pandas as pd 
import numpy as np
import fasttext
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec

global client, df_b
def clean(text):
    res = text.replace("[",'').replace("]","").replace("'","").split(", ")
    text = ''
    for u in res:
        text+=' '+u
    return text

def init(client):
    skills = []
    for item in client['skills'].values:
        skills.append(clean(item))
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(skills)
    return pd.DataFrame(X.toarray(),columns=vectorizer.get_feature_names_out()), vectorizer

def topmin(vect,limit):
    """ Définir les matching les mieux notés"""
    result = []
    a = np.max(vect)
    for _ in range(limit):
        mini= np.min(vect)
        if(mini!=a):
            ind = np.argmin(vect)
            result.append(ind)
            vect[ind]= a
    return result

def define_model():
    model = FastText.load("./IA/word.model")
    #model.save("word.model")
    return model


def match(jober,limit,client,df_bow_sklearn,vectorizer):
    model = define_model() 
    u = jober['skills']
    metier = jober['Job']
    a = vectorizer.transform([u]).toarray()
    dist = []
    result = []
    for vector in df_bow_sklearn.values:
        distance = np.linalg.norm(a-vector)
        dist.append(distance)
    candidates = topmin(dist,100)
    for i in candidates:
        similarity = model.wv.similarity(metier,client.iloc[i]['job'])
        if similarity>limit:
            result.append(i)   
    df = pd.DataFrame(client.iloc[result],index=None)  
    return df.copy()
