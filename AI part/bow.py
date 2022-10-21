#Done
from nltk.tokenize import word_tokenize
import numpy as np
from urllib.request import urlopen
from nltk.stem.porter import PorterStemmer
#import tflearn
#import tensorflow
import random
import json
stemmer = PorterStemmer()

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
        wrds = word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["intent"])


    if intent["intent"] not in labels:
        labels.append(intent["intent"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))


labels = sorted(labels)

#BOW Process

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds =[stemmer.stem(w.lower()) for w in doc]
    #print(wrds)


    for w in words:
        if w in wrds:
            bag.append(1)
            #print(w)
            print(bag)

        else:
            bag.append(0)
            #print(w)
            print(bag)


    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)


