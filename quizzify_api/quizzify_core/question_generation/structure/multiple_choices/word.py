from utils import format_graphy, extract_word_from_name

class Word():

    def __init__(self, graphy, word_class='noun'):
        self.original_graphy = graphy
        self.to_lower = self.get_to_lower()
        self.formatted_search_term = self.format_word_as_search_term()
        self.corrected_graphy = format_graphy(graphy)
        self.word_class = word_class

    def get_to_lower(self):
        return self.original_graphy.lower()

    def replace_spaces_with_underscores(self, term):
        return term.replace(' ', '_')

    def format_word_as_search_term(self):
        word_to_lower = self.to_lower
        return self.replace_spaces_with_underscores(word_to_lower)

    def is_not_the_same_as(self, name):
        return extract_word_from_name(name) != self.formatted_search_term