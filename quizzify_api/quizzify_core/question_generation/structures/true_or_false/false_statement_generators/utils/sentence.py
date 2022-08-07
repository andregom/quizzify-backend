import string
import spacy
from allennlp.predictors.predictor import Predictor

from nltk import tokenize
from nltk.tree import Tree

predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz"#,
    # predictor_name="model.text_field_embedder",
)

nlp = spacy.load('en_core_web_sm')

class Sentence():

    def __init__(self, phrase):
        self.original_phrase = phrase
        self.without_punctuation = self.remove_punctuation()
        self.parser = self.generate_parser()
        self.tree = self.generate_tree()

    def remove_punctuation(self):
        phrase = self.original_phrase
        special_chars = string.punctuation
        filtered_chars = [char for char in phrase if char not in special_chars]
        return ''.join(filtered_chars)

    def generate_parser(self):
        sentence = self.without_punctuation
        return predictor.predict(sentence=sentence)

    def generate_tree(self):
        return self.parser['trees']

    def generate_parser_with_punctuation(self):
        sentence = self.original_phrase.rstrip(string.punctuation)
        return predictor.predict(sentence=sentence)

    def get_formatted_tree(self):
        tree = Tree.fromstring(self.tree)
        return tree.pretty_print()


def test():
    sentence = Sentence('The old: woman was sitting; under a tree, sipping coffe and smiling.')

    tree = sentence.get_formatted_tree()

    print(sentence.without_punctuation)


test()