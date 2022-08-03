from nltk.corpus import wordnet as wn
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')

from utils import format_graphy
from word import Word


def get_similar_words_to(expression, choosen_synset=wn.synsets, lang='por'):
    similar_words = []

    word = Word(expression)

    # if word.is_a_compound_word():
    #     word.format_compund_word()

    term = word.formatted_term
    print(term)
    print(word.in_display_format)
    syns = choosen_synset(term, 'n', lang=lang)
    hypernyms = syns[0].hypernyms()
    hyponyms = hypernyms[0].hyponyms()

    if not hypernyms:
        return similar_words

    # print([(n.name(), n.definition()) for n in hypernyms])
    similar_words = [
        format_graphy(n.name())
        for n in hyponyms
        if word.is_not_the_same_as(n.name())
    ]

    return similar_words


word = 'saltwater fish'
print(get_similar_words_to(word, lang='eng'))

word = 'green'
print(get_similar_words_to(word, lang='eng'))

""" word = 'rede'
print(get_similar_words_to(word))
print()
word = 'banco'
print(get_similar_words_to(word))
print()
word = 'lula'
print(get_similar_words_to(word))
 """
