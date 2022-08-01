def extract_word_from_name(name):
    # print(name.split('.')[0])
    return name.split('.')[0]


def format_graphy(name):
    graphy = extract_word_from_name(name)
    return ' '.join(w.capitalize() for w in graphy.split('_'))
