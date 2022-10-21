#Libraries&Modules
from itertools import count
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
import numpy
from nltk.tokenize import word_tokenize
import numpy as np
from urllib.request import urlopen
#from nltk.stem.porter import PorterStemmer
import tflearn
import tensorflow
import random
import json
import pickle
import random
import math
import sklearn
#stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def read_json(file_name):
    data_file = open(file_name).read()
    data_json = json.loads(data_file)
    words = []
    labels = []
    docs_x = []
    docs_y  = []

    for intent in data_json["intents"]:
        docs_x1=[]
        for pattern in intent["patterns"]:
            pattern=re.sub('[^a-zA-Z]',' ',pattern)
            wrds = word_tokenize(pattern)
            words.extend(wrds)
            docs_y.append(intent["tag"])
            docs_x1.extend(wrds)
        docs_x.append(docs_x1)
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if not w in set(stopwords.words('english')) ]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    with open ("data.pickle","wb") as f:    #wb - write bites
        pickle.dump((words, labels), f)
    return words,labels,docs_x,docs_y

words,labels,docs_x,docs_y = read_json("intents.json")




def computeTF_IDF(words,docs_x):
    tf_bag,idf_bag=[],[]
    countOfDocContainWord ={}
    for doc in docs_x:
        wrds =[lemmatizer.lemmatize(w.lower()) for w in doc if not w in set(stopwords.words('english'))]
        for w in set(wrds):
            if w not in countOfDocContainWord:
                countOfDocContainWord[w] =1
            else:
                countOfDocContainWord[w] +=1

    for doc in docs_x:
        tf,idf=[],[]
        wrds =[lemmatizer.lemmatize(w.lower()) for w in doc if not w in set(stopwords.words('english'))]
        for w in words:
            if w in wrds:
                tf.append(wrds.count(w)/len(wrds))
                idf.append(math.log((len(docs_x))/float(countOfDocContainWord[w])))
            else:
                tf.append(0)
                idf.append(0)
        tf_bag.append(tf)
        idf_bag.append(idf)
    training= np.array(tf_bag) * np.array(idf_bag)
    return training

def comoute_output(labels,docs_x,docs_y):
    output=[]
    for x, _ in enumerate(docs_x):
        output.append(labels.index(docs_y[x]))
    return np.array(output)
output = comoute_output(labels,docs_x,docs_y)
#print(output.shape)


training_tfidf = computeTF_IDF(words,docs_x)
print(training_tfidf.shape)

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
x_train, x_test, y_train, y_test = train_test_split(training_tfidf, output, test_size = 0.20, random_state = 0)
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)
cm = confusion_matrix(y_test, y_pred)
ac= accuracy_score(y_test, y_pred)
print(ac)



