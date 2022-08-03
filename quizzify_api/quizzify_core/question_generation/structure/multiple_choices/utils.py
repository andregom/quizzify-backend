def extract_word_from_name(name):
    # print(name.split('.')[0])
    return name.split('.')[0]


def format_graphy(name):
    graphy = extract_word_from_name(name)
    return ' '.join(w.capitalize() for w in graphy.split('_'))


def extract_element_from(collection, separator = None, index=0):
    if collection:
        if separator is None:
            return collection[index]
            
        return collection.split(separator)[index]
       

    return collection
