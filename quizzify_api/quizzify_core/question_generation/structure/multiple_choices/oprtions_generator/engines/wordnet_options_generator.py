from nltk.corpus import wordnet as wn
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')

from .utils.utils import format_graphy
from .utils.word import Word


def get_similar_words_to(expression, choosen_synset=wn.synsets, lang='eng'):
    similar_words = []

    word = Word(expression)

    term = word.in_search_term_format
    print(term)
    print(word.in_display_format)
    syns = choosen_synset(term, 'n', lang=lang)
    hypernyms = syns[0].hypernyms()
    hyponyms = hypernyms[0].hyponyms()

    if not hypernyms:
        return similar_words

    # print([(n.name(), n.definition()) for n in hypernyms])
    similar_words = [
        format_graphy(h.name())
        for h in hyponyms
        if word.is_not_the_same_as(h.name())
    ]

    return similar_words

def test():
    word = 'saltwater fish'
    print(get_similar_words_to(word))

    word = 'green'
    print(get_similar_words_to(word))

    word = 'rede'
    print(get_similar_words_to(word, lang='por'))
    print()
    word = 'banco'
    print(get_similar_words_to(word, lang='por'))
    print()
    word = 'lula'
    print(get_similar_words_to(word, lang='por'))

