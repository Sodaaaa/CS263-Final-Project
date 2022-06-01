from email import message
import time
from urllib import request
from flask import Flask, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from pysentimiento import create_analyzer
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ClassificationsOptions

app = Flask(__name__)

# pip install tensorflow keras pickle nltk
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
# from keras.optimizers import SGD
import random
import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
# import pickle
import tensorflow as tf

words=[]
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']
msg = []

model = tf.keras.models.load_model('chatbot_model.h5')
intents_file = open('./intents.json').read()
intents = json.loads(intents_file)
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenize each word
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        #add documents in the corpus
        documents.append((word, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
print(len(documents))

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p[:113]]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def responsed(msg1):
    ints = predict_class(msg1)
    print(ints)
    res = getResponse(ints, intents)
    return res


def song_emotion():
    emotion_analyzer = create_analyzer(task="emotion", lang="en")

    # IBM Tone Analyzer
    # authenticator = IAMAuthenticator("5zrGexf4mX0e9LUaxkWB6KLD9ThFWYisj9g-0HAQGuVJ")
    # tone_analyzer = NaturalLanguageUnderstandingV1(
    #     version='2022-04-07',
    #     authenticator=authenticator)
    
    # tone_analyzer.set_service_url("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/4a200f59-699a-4421-afde-5b9af5c06fd7")
    # text = ""
    # for i in msg:
    #     text = text+i

    len1 = len(msg)
    message = ""
    for i in range(5):
        if len1-1-i>=0:
            message = message+ " " + msg[len1-1-i]
        else:
            break
    # tone_analysis = tone_analyzer.analyze(text=message,
                                        #   features=Features(classifications=ClassificationsOptions(model='tone-classifications-en-v1'))).get_result()

    dic1 = dict()
    # emotion=tone_analysis["classifications"][0]["class_name"]
    print(message)
    print("===========",emotion_analyzer.predict(message))
    emotion = emotion_analyzer.predict(message).output
    print(emotion)
    dic1['emotion'] = emotion
    import requests

    url=f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={emotion}&api_key=2d0f2fe468cb70ab69dcabbd31cc38ab&format=json&limit=10"
    response = requests.get(url)
    payload = response.json()
    for i in range(10):
        r=payload['tracks']['track'][i]
        dic1[r['name']] = r['url']
    return dic1


# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model_GPT = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

m = ""
bot_input_ids = None
chat_history_ids = []
new_user_input_ids = None

@app.route('/api/postMessage', methods=["POST"])
def postMessage():
    # Sequential
    global msg
    # m = input("User : ")
    m = request.json['data']['text']
    msg.append(m)
    return

    # DialogGPT
    # global m
    # m = request.json['data']['text']
    # msg.append(m)
    # return

@app.route('/api/getReply', methods=["GET"])
def getReply():
    # Sequential 
    res = responsed(m)
    print("Chatbot : "+res)
    return res

    # # DialogGPT
    # global bot_input_ids
    # global chat_history_ids
    # global new_user_input_ids
    # global m
    # print(m)
    # new_user_input_ids = tokenizer.encode(m+ tokenizer.eos_token, return_tensors='pt')
    # # if bot_input_ids == None:
    # bot_input_ids = new_user_input_ids
    # # else:
    #     # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    # chat_history_ids = model_GPT.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    # print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
    # res = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # print(res)
    # return res

@app.route('/api/getSong', methods=["GET"])
def getSong():
    # Sequential 
    ans = song_emotion()
    print("Emotion : "+ans['emotion'])
    ans.pop('emotion')
    lst = list(ans.keys())
    res = ""
    for i in range(5):
        res += "Song_name : "+lst[i] + ", Song_URL : " + ans[lst[i]] + "\n"
    print(res)
    return res
    