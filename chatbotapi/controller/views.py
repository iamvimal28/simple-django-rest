from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random

from . import translator_service


intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clear_sentence(sentence):
    #Tokenize the sentence and lemmatize and return
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# To return bag of words array: 0 or 1 for words that exist
def bag_of_words(sentence, words, show_details=True):
    sentence_words = clear_sentence(sentence)
    #bag of words = vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    
    return (np.array(bag))

def predict_class(sentence):
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
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

@api_view(['POST'])
def handler(request):
    msg = request.data['msg']
    src_lang = translator_service.detect_language(msg)
    translated_to_english = translator_service.translate(msg,src_lang,'en')

    ints = predict_class(translated_to_english)
    res = getResponse(ints, intents)
    # Translating response to destination language
    dest_res = translator_service.translate(res,'en',src_lang)
    return JsonResponse({"reply":dest_res})
