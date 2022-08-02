from utils import format_graphy, extract_word_from_name

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