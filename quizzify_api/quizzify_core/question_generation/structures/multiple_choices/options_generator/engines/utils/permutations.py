import string

# from .word import Word

def get_all_one_step_edits_of(word):
    letters = string.ascii_lowercase + ' ' + string.punctuation
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L,R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def filter_by_edit_distance(list, original_word):
    one_edit_variations = get_all_one_step_edits_of(original_word)
    return [word for word in list if word not in one_edit_variations]

def index_is_out_of_range(list, index):
    return index >= len(list)

def filter_all_by_edit_distance(list, index=0):
    if index_is_out_of_range(list, index):
        return list
    word = list[index]
    one_edit_variations = get_all_one_step_edits_of(word)
    filtered_list =  [word for word in list if word not in one_edit_variations]
    return filter_all_by_edit_distance(filtered_list, index=index + 1)



# def filter_by_shuffling_and_comparing_terms(list, lexical_item):
#     filtered_list = []
#     original_word = Word(lexical_item)
#     if original_word.is_an_open_compound_word():
#         particles_from_original_word = original_word.get_particles()
#     for word in list:
#         word = Word(word)
#         if word.is_an_open_compound_word():
#             particles = word.get_particles()





def test():
    print(get_all_one_step_edits_of('cat'))