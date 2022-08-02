import requests
import json
import re
import random
import pprint

from utils import format_graphy
from word import Word

def word_is_not_repeated(word, *containers):
    is_not_reapeated = True
    for container in containers:
        is_not_reapeated = is_not_reapeated and word not in container

    return is_not_reapeated

def get_similar_words_to(expression):
    similar_words = []

    word = Word(expression)
    
    term = word.formatted_search_term
    print(term)
    
    url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en%s&limit=5"%(term, term)
    obj = requests.get(url).json()


    # for edge in obj['edges']:
    #     link = edge['end']['term']
    #     print(link)


    for edge in obj['edges']:
        link = edge['end']['term']
        print(link)
        words_alike = []
        url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link, link)
        obj2 = requests.get(url2).json()
        for edge in obj2['edges']:
            word2 = edge['start']['label']
            if word.is_not_the_same_as(word2.lower()):
                words_alike.append(word2)

        print(words_alike)




get_similar_words_to('California')