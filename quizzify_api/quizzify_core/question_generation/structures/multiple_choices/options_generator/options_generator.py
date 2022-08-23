from .engines.sentence_transformers_options_generator import get_similar_options_to
from .engines.utils.word import Word
from .engines.utils import permutations, levenshtein

def get_filtered_similar_options_to(lexical_item):
    
    word = Word(lexical_item)

    distracters = get_similar_options_to(word.on_display_format)

    words_filtrd_by_edit_distance = permutations.filter_by_edit_distance(
        distracters,
        word.original_graphy
    )

    words_filtrd_by_edit_distance = permutations.filter_all_by_edit_distance(
        words_filtrd_by_edit_distance
    )

    filtered_distracters = levenshtein.filter_by_nomralized_distanc(
        words_filtrd_by_edit_distance,
        word.original_graphy,
        0.8
    )

    filtered_distracters = permutations.filter_subsets(
        filtered_distracters
    )

    return distracters# filtered_distracters
