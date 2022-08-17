from .utils import format_graphy, extract_element_from


class Word():

    def __init__(self, graphy, word_class='noun'):
        self.original_graphy = graphy
        self.to_lower = self.get_to_lower()
        self.on_search_term_format = self.format_word_as_search_term()
        self.on_display_format = format_graphy(graphy)
        self.on_display_format_to_lower = self.get_display_format_to_lower()
        self.word_class = word_class

    def get_to_lower(self):
        return self.original_graphy.lower()

    def get_display_format_to_lower(self):
        return self.on_display_format.lower()

    def replace_spaces_with_underscores(self, term):
        return term.replace(' ', '_')

    def format_word_as_search_term(self):
        word_to_lower = self.to_lower
        return self.replace_spaces_with_underscores(word_to_lower)

    def is_not_the_same_as(self, name):
        return extract_element_from(name) != self.on_search_term_format

    def is_an_open_compound_word(self):
        return ' ' in self.original_graphy

    def get_particles(self):
        return self.original_graphy.split(' ')

    def is_not_in(self, list):
        return not self.is_in(list)

    def is_in(self, list):
        return any(
            word for word in list
            if self.on_display_format_to_lower == word.lower()
            or self.to_lower == word.lower()
        )
