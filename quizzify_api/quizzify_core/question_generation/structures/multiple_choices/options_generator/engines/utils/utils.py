from .permutations import get_all_one_step_edits_of


def format_graphy(name):
    graphy = extract_element_from(name, '.')
    return ' '.join(w.capitalize() for w in graphy.split('_'))


def extract_element_from(collection, separator=None, index=0):
    if collection:
        if separator is None:
            return collection[index]

        return collection.split(separator)[index]

    return collection


def unpolute_results_in(list, word):
    one_edit_variations = get_all_one_step_edits_of(word)

    clean_results = [
        word
        for word in list
        if word not in one_edit_variations
    ]

    return clean_results
