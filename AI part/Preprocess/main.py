from urllib.request import urlopen
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
words = set(nltk.corpus.words.words())
lemmatizer = WordNetLemmatizer()


url = "https://raw.githubusercontent.com/Abanoubr/Artive-SCB/main/Customer-Care-Sample-Skill-dialog%20(4).json?token=GHSAT0AAAAAABQTBD7V5X4B5U45KFFISVF4YQ2ZHTA"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

def listToString(s):
    str1 = ""

    for ele in s:
        str1 += ele + " "

    return str1

def check():
    for _responses in data_json["intents"]:
        y = len(data_json["intents"])
        del _responses["description"]

        with open('maindata.json', 'a+') as f:
            f.seek(0)
            f.truncate()
            f.write("{"+ '\n' + '"intents" : [' + "\n")

            for i in range(y):

                    x = (data_json["intents"][i]["examples"])
                    intent_names = data_json["intents"][i]["intent"]

                    print(intent_names)
                    z = len(x)
                    #print(z)
                    #print(type(x))


                    a = listToString([d['text'] for d in x])
                    sentence1 = (a.lower())  # Lower case
                    sentence1 = lemmatizer.lemmatize(sentence1)  # Lemmatizer ( Time consumption is really high )
                    sentence1 = " ".join(w for w in nltk.wordpunct_tokenize(sentence1) if
                                         w.lower() in words or not w.isalpha())  # Non-english words check

                    tokens = nltk.word_tokenize(sentence1)  # Tokenizer
                    tokens = [word for word in sentence1.split() if word not in stop_words]
                    tokens = list(filter(lambda token: token not in string.punctuation, tokens))  # Punctuation
                    _responses.update({"intent": intent_names})
                    _responses.update({"examples": tokens})
                    json_object = json.dumps(_responses)
                    print(json_object)
                    f.write(json_object + '\n')
                    if (i != (y - 1)):
                        f.write(",")

                    """
                    for i in range(z):
                            print(x[i])
                            
                            break
    
    
    
                    
                    res = {}
                    for z in x:
                        res.update(z)
                        print(type(res))
    
                    """
            f.write("]" + "}")
            f.close()
            break

check()

#  O(n^3) complexity !!!