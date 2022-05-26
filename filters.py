# -*- coding: utf-8 -*-

import json
import emoji
from nltk.stem import SnowballStemmer
from spacy_langdetect import LanguageDetector
import spacy
from spacy.language import Language

with open("stopwords.txt") as sw:
    stopwords = json.load(sw)
stopwords = stopwords["words"]


def filter_symbols(word):
    extras = [',','.',':','\'','"','-','¡','¿','#','?','!','(',')','»','«',';','%','{','}','[',']','$','&','/','=',
              '…','+','-','*','_','^','`','|','°','”','✅','‘','“','⁦','—','⏩','⚠️','✌','➡️','♫','♩','❤','▶','√','🤷‍♀️'
              '🆘']

    for e in extras:
        word = word.replace(e,'')

    return emoji.demojize(word, delimiters=("", ""))

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def filter_file(file):
    #stemmer = SnowballStemmer('spanish')

    tweet = [word.lower() for word in file.split()]

    #Filtramos los simbolos
    tweet = [filter_symbols(word) for word in tweet]

    #Filtramos los websites
    tweet = [word for word in tweet if not word.startswith("http") and not word.startswith("@")
             and len(word)]

    #Filtramos los stopwords
    #tweets = [stemmer.stem(word) for word in tweet if word not in stopwords]
    tweets = [normalize(word) for word in tweet if word not in stopwords and not word.isnumeric()]
    
    #filtramos retweets
    if len(tweets)>0 and tweets[0]=="rt":
        tweets.pop(0) 

    return tweets

def get_lang_detector(nlp, name):
    return LanguageDetector()

def getLanguage(text):
    nlp = spacy.load('es_core_news_sm')  # 1
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    doc = nlp(text) #3
    detect_language = doc._.language #4
    return detect_language

