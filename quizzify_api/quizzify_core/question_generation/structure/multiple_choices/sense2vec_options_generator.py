from sense2vec import Sense2Vec

from word import Word
from utils import get_only_first

s2v = Sense2Vec().from_disk('s2v_old')

option = "Donald Trump"

word = Word(option)

term = word.formatted_search_term

print(term)

sense = s2v.get_best_sense(term)

print('Best sense', sense)
most_similar = s2v.most_similar(sense, n=12)
print(most_similar)

for tuple in most_similar:
    entity = get_only_first(tuple)
    term = get_only_first(entity, '|')
    word = Word(term)
    print(word.corrected_graphy)