from nltk.tree import Tree

class TreeClass():

    def __init__(self, tree):
        self.tree = tree

    def get_first_block(self):
        return self.tree[0]

    def get_second_block(self):
        return self.tree[1]

    def get_last_block(self):
        return self.tree[-1]

    def is_a_nominal_phrase(self):
        return self.tree.label() == 'NP'

    def is_a_verbal_phrase(self):
        return self.tree.label() == 'VP'

    def has_no_subtrees(self):
        return len(self.tree.leaves()) == 1
