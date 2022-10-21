from nltk.tokenize import word_tokenize
stemmer = PorterStemmer()
import numpy as np
from urllib.request import urlopen
import tflearn
import tensorflow
import random
import json

url = "https://raw.githubusercontent.com/AlpKaanK/IntentTest/main/Intent%20(1).json?token=GHSAT0AAAAAABQTBD7VZ7ZUGBQVAOCL7C4OYQDYOVA" #fixed
# store the response of URL
response = urlopen(url)
# storing the JSON response
# from url in data
data_json = json.loads(response.read())

words = []
labels = []
docs_x = []
docs_y  = []

for intent in data_json["intents"]:
    for pattern in intent ["text"]:
        wrds = nltk.word_tokenize(pattern)
        word.extend(wrds)
        docs.append(pattern)

    if intent("intent") not in labels:
        labels.append(intent["intent"])

words = [stemmer.stem(w.lower()) for w in words]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(classes))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds =[stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = np.array(output)