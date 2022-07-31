from nltk.corpus import wordnet as wn
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')


def extract_word_from_name(name):
    return name.split('.')[0]


def format_graphy(name):
    graphy = extract_word_from_name(name)
    return ' '.join(w.capitalize() for w in graphy.split('_'))


class Word():

    def __init__(self, graphy, word_class='noun'):
        self.term = graphy.lower()
        self.graphy = format_graphy(graphy)
        self.word_class = word_class

    def is_a_compound_word(self):
        return ' ' in self.term

    def format_compund_word(self):
        self.term = self.term.replace(' ', '_')

    def is_not_the_same_as(self, name):
        return extract_word_from_name(name) != self.term


def get_similar_words_to(idiom, choosen_synset=wn.synsets, lang='por'):
    similar_words = []

    word = Word(idiom)

    if word.is_a_compound_word():
        word.format_compund_word()

    term = word.term
    print(term)
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


word = 'Saltwater fish'
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
