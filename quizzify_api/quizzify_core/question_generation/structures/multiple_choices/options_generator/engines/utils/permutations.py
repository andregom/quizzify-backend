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
    return [word for word in list if word.lower() not in one_edit_variations]

def index_is_out_of_range(list, index):
    return index >= len(list)

def is_a_compound(word):
    return ' ' in word

def filter_all_by_edit_distance(list, index=0):
    if index_is_out_of_range(list, index):
        return list
    original_word = list[index]
    original_word = original_word.lower()
    one_edit_variations = get_all_one_step_edits_of(original_word)
    one_edit_variations.remove(original_word)
    filtered_list = [word for word in list if word.lower() not in one_edit_variations]
    return filter_all_by_edit_distance(filtered_list, index=index + 1)

def word_is_a_subset_of_another(word1, word2):
    set1 = set(word1.split(' '))
    set2 = set(word2.split(' '))
    return word1 != word2 and (set1.issubset(set2) or set2.issubset(set1))

def get_the_subset_between_two_words(word1, word2):
    subset_word = ''
    set1 = set(word1.split(' '))
    set2 = set(word2.split(' '))
    subset_word = word1 if set1.issubset(set2) else word2
    return subset_word



def filter_subsets(list, index=0):
    if index_is_out_of_range(list, index):
        return list
    original_word = list[index]
    if is_a_compound(original_word):
        for word in list:
            if word_is_a_subset_of_another(word, original_word):
                subset_word = get_the_subset_between_two_words(word, original_word)
                print(subset_word)
                if subset_word == original_word:
                    original_word = word

                list.remove(subset_word)

    return filter_subsets(list, index=index + 1)








def test():
    print(get_all_one_step_edits_of('Geroge W'))
    print(filter_by_edit_distance(['Cat'], 'cat'))
    print(filter_all_by_edit_distance(['Cat', 'caty']))
    print(filter_all_by_edit_distance(['Geroge W', 'Geroge W.', 'Geroge W Bush']))