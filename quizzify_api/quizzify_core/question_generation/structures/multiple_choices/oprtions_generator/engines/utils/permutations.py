import string

def get_all_one_step_edits_of(word):
    letters = string.ascii_lowercase + ' ' + string.punctuation
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L,R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def filter_by_edit_distance(list, word):
    one_edit_variations = get_all_one_step_edits_of(word)
    return [word for word in list if word not in one_edit_variations]

def test():
    print(get_all_one_step_edits_of('cat'))