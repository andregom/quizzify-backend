from pathlib import Path
from sense2vec import Sense2Vec

from word import Word
from utils import extract_element_from

path = Path(__file__).parent.joinpath('s2v_old')
s2v = Sense2Vec().from_disk(path)

def get_similar_options_to(idiomatic_expression, s2v_instance=s2v):
    options_alike = []

    word = Word(idiomatic_expression)

    term = word.in_search_term_format

    print(term)

    sense = s2v_instance.get_best_sense(term)

    print('Best sense', extract_element_from(sense, '|', 1))
    most_similar = s2v_instance.most_similar(sense, n=12) \
        if sense is not None else []

    for tuple in most_similar:
        entity = extract_element_from(tuple)
        term = extract_element_from(entity, '|')
        word = Word(term)
        if word.is_not_in(options_alike):
            options_alike.append(word.in_display_format)

    return options_alike

def test():
    option = "Donald Trump"
    print(*get_similar_options_to(option), sep = ", ")

    option = "Lula"
    print(*get_similar_options_to(option), sep = ", ")

    option = "Dilma Rousef"
    print(*get_similar_options_to(option), sep = ", ")

    option = "natural language processing"
    print(*get_similar_options_to(option), sep = ", ")

    option = "Go"
    print(*get_similar_options_to(option), sep = ", ")

    option = "Golang"
    print(*get_similar_options_to(option), sep = ", ")