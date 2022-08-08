import string
import spacy
from allennlp.predictors.predictor import Predictor

from nltk import tokenize
from nltk.tree import Tree

from .tree import TreeClass

predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz"  # ,
    # predictor_name="model.text_field_embedder",
)

nlp = spacy.load('en_core_web_sm')


class Sentence():

    def __init__(self, phrase):
        self.original_phrase = phrase
        self.special_chars_removed = self.remove_punctuation()
        self.parser = self.generate_parser()
        self.tree = self.generate_tree()

        self.last_nominal_phrase_tree, self.last_verbal_phrase_tree = \
            self.get_right_most_nominal_and_verbal_phrase()
        self.last_nominal_phrase = self.flatten_tree(
            self.last_nominal_phrase_tree
        )
        self.last_verbal_phrase = self.flatten_tree(
            self.last_verbal_phrase_tree
        )

        self.partial_sentence = self.cut_last_longest_block()

    def remove_punctuation(self):
        phrase = self.original_phrase
        special_chars = string.punctuation
        filtered_chars = [char for char in phrase if char not in special_chars]
        return ''.join(filtered_chars)

    def generate_parser(self):
        sentence = self.special_chars_removed
        return predictor.predict(sentence=sentence)

    def generate_tree(self):
        tree_as_string = self.parser['trees']
        return Tree.fromstring(tree_as_string)

    def _get_right_most_recursive(
        self,
        tree,
        last_nominal_phrase=None,
        last_verbal_phrase=None
    ):
        current_tree = TreeClass(tree)
        if current_tree.has_no_subtrees():
            return last_nominal_phrase, last_verbal_phrase
        last_block = current_tree.get_last_block()
        last_subtree = TreeClass(last_block)
        if last_subtree.is_a_nominal_phrase():
            last_nominal_phrase = last_subtree.tree
        elif last_subtree.is_a_verbal_phrase():
            last_verbal_phrase = last_subtree.tree

        return self._get_right_most_recursive(
            last_subtree.tree,
            last_nominal_phrase,
            last_verbal_phrase
        )

    def get_right_most_nominal_and_verbal_phrase(self):
        return self._get_right_most_recursive(self.tree)

    def flatten_tree(self, tree):
        final_phrase = None
        if tree is not None:
            phrase = [" ".join(t.leaves()) for t in list(tree)]
            final_phrase = [" ".join(phrase)]
            final_phrase = final_phrase[0]
        return final_phrase

    def cut_last_longest_block(self):
        nominal_phrase = self.last_nominal_phrase
        verbal_phrase = self.last_verbal_phrase

        longest_chunk = max(nominal_phrase, verbal_phrase, key=len)
        longest_chunk = ' ' + longest_chunk

        return self.original_phrase[:-len(longest_chunk)]


    def generate_parser_with_punctuation(self):
        sentence = self.original_phrase.rstrip(string.punctuation)
        return predictor.predict(sentence=sentence)

    def visualize_tree(self):
        self.tree.pretty_print()


def test(sentence):
    original_sentence = Sentence(sentence)

    # original_sentence.visualize_tree()

    print(original_sentence.special_chars_removed)

    print(original_sentence.last_nominal_phrase)
    print(original_sentence.last_verbal_phrase)
    print(original_sentence.cut_last_longest_block())


# test('The old woman was sitting under a tree and sipping coffee.')
# print()
# test('The old woman was sitting at a chair, drinking tea and reading a book.')
